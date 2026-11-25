"""Generate 16 exact-Z/Q VALIANT-HIER-CERT-1.0 certificates and 4 reproducible experiments for Paper 20.
Author: Lluis Eriksson
"""
from __future__ import annotations

import json
import math
import pathlib
import sys
import time
from fractions import Fraction
from typing import Any, Dict, List, Tuple

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.valiant_certifier import SCHEMA_VERSION, verify_valiant_hier_certificate_exact
from src.valiant_exact import (
    binary_tree_state_sum_dp_exact,
    fmt_rat,
    grid_state_sum_transfer_exact,
    path_state_sum_abp_exact,
    path_state_sum_bisection_exact,
)

RESULTS = ROOT / "results"
CERTS = RESULTS / "certificates"
CERTS.mkdir(parents=True, exist_ok=True)


def _det_rat(seed: int) -> Fraction:
    num = ((seed * 17 + 5) % 9) - 4
    den = 1 if (seed % 3 != 0) else 2
    return Fraction(num, den)


def _build_path_cert(name: str, d: int, q: int, salt: int) -> Dict[str, Any]:
    lv = [_det_rat(salt * 31 + i) for i in range(q)]
    rv = [_det_rat(salt * 53 + i + 7) for i in range(q)]
    mats = [
        [[_det_rat(salt * 97 + t * 19 + i * 5 + j) for j in range(q)] for i in range(q)]
        for t in range(d - 2)
    ]
    val = path_state_sum_abp_exact(lv, mats, rv)
    assert val == path_state_sum_bisection_exact(lv, mats, rv)
    return {
        "schema": SCHEMA_VERSION,
        "mode": "path_abp_vs_bisection_exact",
        "name": name,
        "num_vertices_d": d,
        "states_q": q,
        "left_vec": [fmt_rat(x) for x in lv],
        "matrices": [[[fmt_rat(x) for x in row] for row in M] for M in mats],
        "right_vec": [fmt_rat(x) for x in rv],
        "claimed_state_sum": fmt_rat(val),
    }


def _build_tree_cert(name: str, L: int, q: int, salt: int) -> Dict[str, Any]:
    n_leaves = 1 << (L - 1)
    n_int = n_leaves - 2
    leaves = [[_det_rat(salt * 23 + k * 7 + i) for i in range(q)] for k in range(n_leaves)]
    internals = [
        [
            [[_det_rat(salt * 41 + t * 29 + a * 11 + b * 5 + c) for c in range(q)] for b in range(q)]
            for a in range(q)
        ]
        for t in range(n_int)
    ]
    root_m = [[_det_rat(salt * 67 + a * 13 + b) for b in range(q)] for a in range(q)]
    val = binary_tree_state_sum_dp_exact(L, q, leaves, internals, root_m)
    return {
        "schema": SCHEMA_VERSION,
        "mode": "binary_tree_circuit_dp_exact",
        "name": name,
        "levels_L": L,
        "states_q": q,
        "leaf_vecs": [[fmt_rat(x) for x in v] for v in leaves],
        "internal_tensors": [[[[fmt_rat(x) for x in row] for row in sl] for sl in T] for T in internals],
        "root_mat": [[fmt_rat(x) for x in row] for row in root_m],
        "claimed_state_sum": fmt_rat(val),
    }


def _build_grid_cert(name: str, rows: int, cols: int, q: int, salt: int) -> Dict[str, Any]:
    tables: Dict[Tuple[int, int], List[Fraction]] = {}
    tables_json: Dict[str, List[str]] = {}
    for r in range(rows):
        for c in range(cols):
            deg = int(r > 0) + int(c > 0) + int(r < rows - 1) + int(c < cols - 1)
            tlen = q ** deg
            tbl = [Fraction(((salt * 19 + r * 11 + c * 7 + idx * 3) % 5) - 2, 1) for idx in range(tlen)]
            tables[(r, c)] = tbl
            tables_json[f"{r},{c}"] = [fmt_rat(x) for x in tbl]
    val = grid_state_sum_transfer_exact(rows, cols, q, tables)
    return {
        "schema": SCHEMA_VERSION,
        "mode": "grid_transfer_vnp_exact",
        "name": name,
        "rows": rows,
        "cols": cols,
        "states_q": q,
        "vertex_tables": tables_json,
        "claimed_state_sum": fmt_rat(val),
    }


def _build_barrier_cert(
    name: str, table: List[int], gn: int, tL: int, bn: int, k: int, s1: int, s2: int, s3: int
) -> Dict[str, Any]:
    return {
        "schema": SCHEMA_VERSION,
        "mode": "hierarchy_separation_barrier_exact",
        "name": name,
        "selector_table": [str(x) for x in table],
        "grid_n": gn,
        "tree_levels_L": tL,
        "base_n": bn,
        "poly_exp_k": k,
        "exp_s1_vf": s1,
        "exp_s2_vbp": s2,
        "exp_s3_vp": s3,
    }


def main() -> None:
    certs: List[tuple[str, Dict[str, Any]]] = [
        # Mode 1: Path state sum ABP == bisection (VF < VBP)
        ("path_d4_q2.cert.json", _build_path_cert("path_d4_q2", 4, 2, 1)),
        ("path_d8_q3.cert.json", _build_path_cert("path_d8_q3", 8, 3, 2)),
        ("path_d16_q4.cert.json", _build_path_cert("path_d16_q4", 16, 4, 3)),
        ("path_d24_q5.cert.json", _build_path_cert("path_d24_q5", 24, 5, 4)),
        # Mode 2: Complete binary tree bottom-up VP circuit DP (VBP < VP)
        ("tree_L2_q2.cert.json", _build_tree_cert("tree_L2_q2", 2, 2, 1)),
        ("tree_L3_q2.cert.json", _build_tree_cert("tree_L3_q2", 3, 2, 2)),
        ("tree_L4_q3.cert.json", _build_tree_cert("tree_L4_q3", 4, 3, 3)),
        ("tree_L5_q3.cert.json", _build_tree_cert("tree_L5_q3", 5, 3, 4)),
        # Mode 3: Square/rect grid boundary-frontier transfer DP (VP < VNP)
        ("grid_2x2_q2.cert.json", _build_grid_cert("grid_2x2_q2", 2, 2, 2, 1)),
        ("grid_3x3_q2.cert.json", _build_grid_cert("grid_3x3_q2", 3, 3, 2, 2)),
        ("grid_4x4_q2.cert.json", _build_grid_cert("grid_4x4_q2", 4, 4, 2, 3)),
        ("grid_3x3_q3.cert.json", _build_grid_cert("grid_3x3_q3", 3, 3, 3, 4)),
        # Mode 4: Strict hierarchy separation & char-free VNP selector barriers
        ("hier_barrier_n4.cert.json", _build_barrier_cert("hier_barrier_n4", [3, -5, 7, 11], 4, 4, 4, 2, 3, 5, 8)),
        ("hier_barrier_n8.cert.json", _build_barrier_cert("hier_barrier_n8", [-2, 9, -4, 13], 8, 6, 8, 3, 5, 8, 12)),
        ("hier_barrier_n16.cert.json", _build_barrier_cert("hier_barrier_n16", [17, -19, 23, -29], 16, 8, 16, 4, 6, 10, 15)),
        ("hier_barrier_n32.cert.json", _build_barrier_cert("hier_barrier_n32", [101, -203, 307, 409], 32, 10, 32, 5, 8, 13, 20)),
    ]

    # Experiment 1: Certified Atlas (16 exact-Q certificates)
    atlas_rows = []
    for fname, cert in certs:
        (CERTS / fname).write_text(json.dumps(cert, indent=2) + "\n", encoding="utf-8")
        t0 = time.perf_counter()
        summary = verify_valiant_hier_certificate_exact(cert)
        dt_ms = (time.perf_counter() - t0) * 1000.0
        atlas_rows.append({"file": fname, "mode": cert["mode"], "verify_ms": round(dt_ms, 4), "summary": summary})
    (RESULTS / "exp1_certified_atlas.json").write_text(
        json.dumps({"experiment": "exp1_certified_atlas", "count": len(atlas_rows), "rows": atlas_rows}, indent=2) + "\n",
        encoding="utf-8",
    )

    # Experiment 2: Exact Path (ABP vs Bisection) & Binary Tree (VP Circuit DP) Scaling
    path_tree_rows = []
    for L in (2, 3, 4, 5, 6):
        d = (1 << L) - 1  # match vertex count of L-level binary tree
        c_p = _build_path_cert(f"pt_p_{d}", d, 3, L + 10)
        c_t = _build_tree_cert(f"pt_t_{L}", L, 3, L + 20)
        t0 = time.perf_counter()
        verify_valiant_hier_certificate_exact(c_p)
        p_ms = (time.perf_counter() - t0) * 1000.0
        t1 = time.perf_counter()
        verify_valiant_hier_certificate_exact(c_t)
        t_ms = (time.perf_counter() - t1) * 1000.0
        path_tree_rows.append({
            "levels_L": L,
            "vertices": d,
            "q": 3,
            "path_verify_ms": round(p_ms, 4),
            "tree_verify_ms": round(t_ms, 4),
            "abp_edges": (d - 2) * 9,
            "vp_gate_budget": ((1 << (L - 1)) - 2) * 27 + 9,
        })
    (RESULTS / "exp2_path_and_tree_scaling.json").write_text(
        json.dumps({"experiment": "exp2_path_and_tree_scaling", "rows": path_tree_rows}, indent=2) + "\n",
        encoding="utf-8",
    )

    # Experiment 3: Square Grid Exact Transfer-Matrix Contraction Scaling (2x2 to 5x5 at q=2)
    grid_rows = []
    for n in (2, 3, 4, 5):
        c_g = _build_grid_cert(f"grid_{n}x{n}", n, n, 2, n + 30)
        t0 = time.perf_counter()
        res = verify_valiant_hier_certificate_exact(c_g)
        dt_ms = (time.perf_counter() - t0) * 1000.0
        grid_rows.append({
            "grid_n": n,
            "num_vertices": n * n,
            "num_edges": 2 * n * (n - 1),
            "brute_force_states": 1 << (2 * n * (n - 1)),
            "frontier_dim": res["frontier_dim"],
            "verify_ms": round(dt_ms, 4),
            "state_sum": res["state_sum"],
        })
    (RESULTS / "exp3_grid_transfer_scaling.json").write_text(
        json.dumps({"experiment": "exp3_grid_transfer_scaling", "rows": grid_rows}, indent=2) + "\n",
        encoding="utf-8",
    )

    # Experiment 4: OpenAI Theorem 1.1 Asymptotic Superpolynomial Exponent Comparison (illustrative c=1)
    asymp_rows = []
    for log2_n in [16, 32, 64, 128, 256, 512, 1024]:
        ln_n = log2_n * math.log(2.0)
        ln_ln_n = math.log(ln_n)
        asymp_rows.append({
            "log2_n": log2_n,
            "path_formula_exp": round(ln_ln_n, 4),          # Omega(log log n)
            "tree_abp_exp": round(math.sqrt(ln_ln_n), 4),   # Omega(sqrt(log log n))
            "grid_circuit_exp": round(ln_n ** (1.0 / 12.0), 4),  # Omega((log n)^(1/12))
            "fixed_poly_const": 2.0,
        })
    (RESULTS / "exp4_hierarchy_exponents.json").write_text(
        json.dumps({"experiment": "exp4_hierarchy_exponents", "rows": asymp_rows}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[PASS] Generated {len(atlas_rows)} certificates and all 4 experiment JSONs.")


if __name__ == "__main__":
    main()
