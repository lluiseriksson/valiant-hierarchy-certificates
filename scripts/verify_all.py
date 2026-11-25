"""One-command Gate-2 reproducibility verifier for Paper 20.
Checks:
  1. Zero-dependency Lean 4 kernel build + axiom audit (18/18, 0 warnings, 0 sorry, 0 Classical.choice)
  2. All 16 exact-Q VALIANT-HIER-CERT-1.0 certificates (0 floats)
  3. Full pytest suite (brute-force q^E cross-checks + 54/54 live red-team attacks)
  4. SHA-256 manifest verification across all tracked files

Author: Lluis Eriksson
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.valiant_certifier import verify_valiant_hier_certificate_exact

MANIFEST_PATH = ROOT / "SHA256SUMS.json"
TRACKED_GLOBS = [
    "LICENSE",
    "README.md",
    "pyproject.toml",
    "lean/lean-toolchain",
    "lean/lakefile.lean",
    "lean/ValiantHierarchy.lean",
    "lean/AuditAxioms.lean",
    "src/__init__.py",
    "src/valiant_exact.py",
    "src/valiant_certifier.py",
    "scripts/run_all_experiments.py",
    "scripts/make_figures.py",
    "scripts/verify_all.py",
    "tests/test_suite.py",
    "results/*.json",
    "results/certificates/*.cert.json",
    "paper/main.tex",
    "paper/references.bib",
    "paper/figures/*.png",
]


def _sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tracked_files() -> list[pathlib.Path]:
    out = []
    for pattern in TRACKED_GLOBS:
        out.extend(sorted(ROOT.glob(pattern)))
    return sorted(set(p for p in out if p.is_file()))


def check_lean() -> None:
    lean_dir = ROOT / "lean"
    r1 = subprocess.run(["lake", "build"], cwd=lean_dir, capture_output=True, text=True, check=False)
    if r1.returncode != 0:
        raise RuntimeError(f"lake build failed:\n{r1.stdout}\n{r1.stderr}")
    if "warning:" in r1.stdout or "warning:" in r1.stderr:
        raise RuntimeError(f"Lean warnings detected:\n{r1.stdout}\n{r1.stderr}")
    r2 = subprocess.run(["lake", "env", "lean", "-j", "1", "AuditAxioms.lean"], cwd=lean_dir, capture_output=True, text=True, check=False)
    if r2.returncode != 0:
        raise RuntimeError(f"AuditAxioms failed:\n{r2.stdout}\n{r2.stderr}")
    combined = r2.stdout + r2.stderr
    for forbidden in ("sorryAx", "Classical.choice", "Lean.ofReduceBool"):
        if forbidden in combined:
            raise RuntimeError(f"Forbidden axiom {forbidden} found:\n{combined}")
    lines = [ln for ln in r2.stdout.splitlines() if "ValiantHierarchy." in ln]
    if len(lines) != 18:
        raise RuntimeError(f"Expected 18 audited theorems, found {len(lines)}")
    print("[PASS] Lean 4 kernel: 18/18 theorems, 0 warnings, 0 sorry, 0 Classical.choice")


def check_certs() -> None:
    files = sorted((ROOT / "results" / "certificates").glob("*.cert.json"))
    if len(files) != 16:
        raise RuntimeError(f"Expected 16 certificates, found {len(files)}")
    for f in files:
        res = verify_valiant_hier_certificate_exact(json.loads(f.read_text(encoding="utf-8")))
        assert res["verified"] is True
    print("[PASS] Exact-Q certificates: 16/16 independently verified (0 floats)")


def check_pytest() -> None:
    r = subprocess.run([sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "-q"], cwd=ROOT, capture_output=True, text=True, check=False)
    if r.returncode != 0:
        raise RuntimeError(f"pytest failed:\n{r.stdout}\n{r.stderr}")
    print(f"[PASS] pytest: {r.stdout.strip()}")


def write_or_check_manifest(write: bool) -> None:
    files = _tracked_files()
    current = {p.relative_to(ROOT).as_posix(): _sha256(p) for p in files}
    if write:
        MANIFEST_PATH.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"[PASS] Wrote SHA256SUMS.json ({len(current)} files)")
        return
    if not MANIFEST_PATH.exists():
        raise RuntimeError("SHA256SUMS.json missing; run with --write-manifest first")
    expected = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if expected != current:
        diff_keys = sorted(set(expected.keys()) ^ set(current.keys()))
        bad_vals = [k for k in expected if k in current and expected[k] != current[k]]
        raise RuntimeError(f"SHA256SUMS mismatch: key_diff={diff_keys}, hash_diff={bad_vals}")
    print(f"[PASS] SHA256SUMS.json: {len(current)}/{len(current)} hashes match")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-manifest", action="store_true")
    args = ap.parse_args()
    check_lean()
    check_certs()
    check_pytest()
    write_or_check_manifest(args.write_manifest)
    print("=== ALL PAPER 20 GATE-2 VERIFICATION CHECKS PASSED ===")


if __name__ == "__main__":
    main()
