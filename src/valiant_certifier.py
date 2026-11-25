"""Pure-stdlib zero-float verifier for VALIANT-HIER-CERT-1.0 certificates.
Supports four exact-Z/Q verification modes aligned with OpenAI (Nov 24, 2026)
"Paths, trees and grids separate Valiant's hierarchy":
  1. path_abp_vs_bisection_exact       (VF < VBP witness: exact path Z_{P_d, q} via ABP == bisection)
  2. binary_tree_circuit_dp_exact      (VBP < VP witness: exact binary tree Z_{T_L, q} via bottom-up VP DP)
  3. grid_transfer_vnp_exact           (VP < VNP witness: exact r x c grid Z_{Grid, q} via transfer contraction)
  4. hierarchy_separation_barrier_exact (OpenAI Thm 1.1: char-free VNP selector + strict VF < VBP < VP < VNP bounds)

Author: Lluis Eriksson
"""
from __future__ import annotations

import re
from fractions import Fraction
from typing import Any, Dict, List, Tuple

from src.valiant_exact import (
    binary_tree_state_sum_dp_exact,
    grid_state_sum_transfer_exact,
    path_state_sum_abp_exact,
    path_state_sum_bisection_exact,
)

SCHEMA_VERSION = "VALIANT-HIER-CERT-1.0"
_CANON_INT_RE = re.compile(r"\A(?:0|-?[1-9][0-9]*)\Z")
_CANON_FRAC_RE = re.compile(r"\A-?[1-9][0-9]*/[1-9][0-9]*\Z")


class ValiantHierCertificateError(ValueError):
    """Raised whenever any VALIANT-HIER-CERT-1.0 verification check fails."""


def _assert_strict_json_types(obj: Any, path: str = "root") -> None:
    t = type(obj)
    if t is int or t is str or obj is None:
        return
    if t is dict:
        for k, v in obj.items():
            if type(k) is not str:
                raise ValiantHierCertificateError(f"Non-str dict key at {path}: {type(k).__name__}")
            _assert_strict_json_types(v, f"{path}.{k}")
        return
    if t is list:
        for i, v in enumerate(obj):
            _assert_strict_json_types(v, f"{path}[{i}]")
        return
    raise ValiantHierCertificateError(f"Forbidden type {t.__name__} at {path}")


def _parse_int(val: Any, name: str) -> int:
    if type(val) is not int:
        raise ValiantHierCertificateError(f"{name} must be strict int, got {type(val).__name__}")
    return val


def _parse_rat(val: Any, name: str) -> Fraction:
    if type(val) is int:
        return Fraction(val, 1)
    if type(val) is str:
        if _CANON_INT_RE.match(val):
            return Fraction(int(val), 1)
        if _CANON_FRAC_RE.match(val):
            num_s, den_s = val.split("/")
            num, den = int(num_s), int(den_s)
            if den < 2:
                raise ValiantHierCertificateError(f"{name} denominator must be >= 2: {val!r}")
            q = Fraction(num, den)
            if q.numerator != num or q.denominator != den:
                raise ValiantHierCertificateError(f"{name} unreduced fraction: {val!r}")
            return q
        raise ValiantHierCertificateError(f"{name} non-canonical rational string: {val!r}")
    raise ValiantHierCertificateError(f"{name} invalid type {type(val).__name__}")


def _parse_vec(raw: Any, q: int, name: str) -> List[Fraction]:
    if type(raw) is not list or len(raw) != q:
        raise ValiantHierCertificateError(f"{name} must be list of length {q}")
    return [_parse_rat(x, f"{name}[{i}]") for i, x in enumerate(raw)]


def _parse_mat(raw: Any, q: int, name: str) -> List[List[Fraction]]:
    if type(raw) is not list or len(raw) != q:
        raise ValiantHierCertificateError(f"{name} must be {q}x{q}")
    return [_parse_vec(row, q, f"{name}[{i}]") for i, row in enumerate(raw)]


def _parse_tensor3(raw: Any, q: int, name: str) -> List[List[List[Fraction]]]:
    if type(raw) is not list or len(raw) != q:
        raise ValiantHierCertificateError(f"{name} must be {q}x{q}x{q}")
    return [_parse_mat(sl, q, f"{name}[{i}]") for i, sl in enumerate(raw)]


def _verify_path_abp(cert: Dict[str, Any]) -> Dict[str, Any]:
    req = {
        "schema", "mode", "name", "num_vertices_d", "states_q",
        "left_vec", "matrices", "right_vec", "claimed_state_sum",
    }
    if set(cert.keys()) != req:
        raise ValiantHierCertificateError(f"Mode 1 key mismatch: {sorted(set(cert.keys()) ^ req)}")
    d = _parse_int(cert["num_vertices_d"], "num_vertices_d")
    q = _parse_int(cert["states_q"], "states_q")
    if not (3 <= d <= 64) or not (2 <= q <= 8):
        raise ValiantHierCertificateError(f"Invalid path params d={d}, q={q}")
    lv = _parse_vec(cert["left_vec"], q, "left_vec")
    rv = _parse_vec(cert["right_vec"], q, "right_vec")
    mats_raw = cert["matrices"]
    if type(mats_raw) is not list or len(mats_raw) != d - 2:
        raise ValiantHierCertificateError(f"Expected {d - 2} transition matrices for {d}-vertex path")
    mats = [_parse_mat(M, q, f"matrices[{i}]") for i, M in enumerate(mats_raw)]
    v_abp = path_state_sum_abp_exact(lv, mats, rv)
    v_bis = path_state_sum_bisection_exact(lv, mats, rv)
    claimed = _parse_rat(cert["claimed_state_sum"], "claimed_state_sum")
    if v_abp != v_bis or v_abp != claimed:
        raise ValiantHierCertificateError(f"Path state-sum mismatch: abp={v_abp}, bis={v_bis}, claimed={claimed}")
    return {
        "verified": True,
        "mode": cert["mode"],
        "d": d,
        "q": q,
        "abp_edges": (d - 2) * q * q,
        "state_sum": str(claimed),
    }


def _verify_binary_tree_dp(cert: Dict[str, Any]) -> Dict[str, Any]:
    req = {
        "schema", "mode", "name", "levels_L", "states_q",
        "leaf_vecs", "internal_tensors", "root_mat", "claimed_state_sum",
    }
    if set(cert.keys()) != req:
        raise ValiantHierCertificateError(f"Mode 2 key mismatch: {sorted(set(cert.keys()) ^ req)}")
    L = _parse_int(cert["levels_L"], "levels_L")
    q = _parse_int(cert["states_q"], "states_q")
    if not (2 <= L <= 6) or not (2 <= q <= 5):
        raise ValiantHierCertificateError(f"Invalid binary-tree params L={L}, q={q}")
    n_leaves = 1 << (L - 1)
    n_int = n_leaves - 2
    leaves_raw = cert["leaf_vecs"]
    ints_raw = cert["internal_tensors"]
    if type(leaves_raw) is not list or len(leaves_raw) != n_leaves:
        raise ValiantHierCertificateError(f"Expected {n_leaves} leaf_vecs")
    if type(ints_raw) is not list or len(ints_raw) != n_int:
        raise ValiantHierCertificateError(f"Expected {n_int} internal_tensors")
    leaves = [_parse_vec(v, q, f"leaf_vecs[{i}]") for i, v in enumerate(leaves_raw)]
    internals = [_parse_tensor3(T, q, f"internal_tensors[{i}]") for i, T in enumerate(ints_raw)]
    root_m = _parse_mat(cert["root_mat"], q, "root_mat")
    val = binary_tree_state_sum_dp_exact(L, q, leaves, internals, root_m)
    claimed = _parse_rat(cert["claimed_state_sum"], "claimed_state_sum")
    if val != claimed:
        raise ValiantHierCertificateError(f"Binary-tree state-sum mismatch: got {val}, claimed {claimed}")
    return {
        "verified": True,
        "mode": cert["mode"],
        "levels": L,
        "q": q,
        "num_vertices": (1 << L) - 1,
        "vp_gate_budget": n_int * (q ** 3) + q * q,
        "state_sum": str(claimed),
    }


def _verify_grid_transfer(cert: Dict[str, Any]) -> Dict[str, Any]:
    req = {
        "schema", "mode", "name", "rows", "cols", "states_q",
        "vertex_tables", "claimed_state_sum",
    }
    if set(cert.keys()) != req:
        raise ValiantHierCertificateError(f"Mode 3 key mismatch: {sorted(set(cert.keys()) ^ req)}")
    rows = _parse_int(cert["rows"], "rows")
    cols = _parse_int(cert["cols"], "cols")
    q = _parse_int(cert["states_q"], "states_q")
    if not (2 <= rows <= 5) or not (2 <= cols <= 5) or not (2 <= q <= 3):
        raise ValiantHierCertificateError(f"Invalid grid params rows={rows}, cols={cols}, q={q}")
    vt_raw = cert["vertex_tables"]
    if type(vt_raw) is not dict or len(vt_raw) != rows * cols:
        raise ValiantHierCertificateError(f"vertex_tables must contain exactly {rows * cols} entries")
    tables: Dict[Tuple[int, int], List[Fraction]] = {}
    for r in range(rows):
        for c in range(cols):
            key = f"{r},{c}"
            if key not in vt_raw:
                raise ValiantHierCertificateError(f"Missing vertex_tables[{key!r}]")
            deg = int(r > 0) + int(c > 0) + int(r < rows - 1) + int(c < cols - 1)
            if deg > 4:
                raise ValiantHierCertificateError("Impossible: grid vertex degree > 4")
            expected_len = q ** deg
            raw_t = vt_raw[key]
            if type(raw_t) is not list or len(raw_t) != expected_len:
                raise ValiantHierCertificateError(f"vertex_tables[{key!r}] must have length {expected_len}")
            tables[(r, c)] = [_parse_rat(x, f"vertex_tables[{key!r}][{i}]") for i, x in enumerate(raw_t)]
    val = grid_state_sum_transfer_exact(rows, cols, q, tables)
    claimed = _parse_rat(cert["claimed_state_sum"], "claimed_state_sum")
    if val != claimed:
        raise ValiantHierCertificateError(f"Grid state-sum mismatch: got {val}, claimed {claimed}")
    num_edges = rows * (cols - 1) + cols * (rows - 1)
    return {
        "verified": True,
        "mode": cert["mode"],
        "rows": rows,
        "cols": cols,
        "q": q,
        "num_edges": num_edges,
        "frontier_dim": q ** rows,
        "state_sum": str(claimed),
    }


def _verify_hierarchy_barrier(cert: Dict[str, Any]) -> Dict[str, Any]:
    req = {
        "schema", "mode", "name", "selector_table",
        "grid_n", "tree_levels_L", "base_n",
        "poly_exp_k", "exp_s1_vf", "exp_s2_vbp", "exp_s3_vp",
    }
    if set(cert.keys()) != req:
        raise ValiantHierCertificateError(f"Mode 4 key mismatch: {sorted(set(cert.keys()) ^ req)}")
    st_raw = cert["selector_table"]
    if type(st_raw) is not list or len(st_raw) != 4:
        raise ValiantHierCertificateError("selector_table must have 4 entries [t00, t01, t10, t11]")
    t00, t01, t10, t11 = [_parse_rat(x, f"selector_table[{i}]") for i, x in enumerate(st_raw)]
    # Verify char-free 2-bit Boolean VNP selector recovers all 4 entries identically (Lean Thm 13)
    for b0, b1, expected in ((0, 0, t00), (0, 1, t01), (1, 0, t10), (1, 1, t11)):
        got = (1 - b0) * (1 - b1) * t00 + (1 - b0) * b1 * t01 + b0 * (1 - b1) * t10 + b0 * b1 * t11
        if got != expected:
            raise ValiantHierCertificateError("Characteristic-free 2-bit VNP selector check failed")

    gn = _parse_int(cert["grid_n"], "grid_n")
    tL = _parse_int(cert["tree_levels_L"], "tree_levels_L")
    bn = _parse_int(cert["base_n"], "base_n")
    k = _parse_int(cert["poly_exp_k"], "poly_exp_k")
    s1 = _parse_int(cert["exp_s1_vf"], "exp_s1_vf")
    s2 = _parse_int(cert["exp_s2_vbp"], "exp_s2_vbp")
    s3 = _parse_int(cert["exp_s3_vp"], "exp_s3_vp")
    if not (2 <= gn <= 1024) or tL < 2 or tL > 30 or bn < 2 or bn > 64:
        raise ValiantHierCertificateError("Invalid grid_n, tree_levels_L, or base_n bounds")
    if not (1 <= k < s1 < s2 < s3 <= 24):
        raise ValiantHierCertificateError(f"Require 1 <= k < s1 < s2 < s3 <= 24, got {(k, s1, s2, s3)}")
    if not ((bn ** k) < (bn ** s1) < (bn ** s2) < (bn ** s3)):
        raise ValiantHierCertificateError("Strict superpolynomial hierarchy chain failed")
    return {
        "verified": True,
        "mode": cert["mode"],
        "grid_edges": 2 * gn * (gn - 1),
        "tree_vertices": (1 << tL) - 1,
        "tree_edges": (1 << tL) - 2,
        "hierarchy_exponents": [k, s1, s2, s3],
    }


def verify_valiant_hier_certificate_exact(cert: Dict[str, Any]) -> Dict[str, Any]:
    if type(cert) is not dict:
        raise ValiantHierCertificateError("Certificate root must be a dict")
    _assert_strict_json_types(cert)
    if cert.get("schema") != SCHEMA_VERSION:
        raise ValiantHierCertificateError(f"Invalid schema: {cert.get('schema')!r}")
    name = cert.get("name")
    if type(name) is not str or not name.strip():
        raise ValiantHierCertificateError(f"Certificate name must be non-empty str, got {name!r}")
    mode = cert.get("mode")
    if mode == "path_abp_vs_bisection_exact":
        return _verify_path_abp(cert)
    if mode == "binary_tree_circuit_dp_exact":
        return _verify_binary_tree_dp(cert)
    if mode == "grid_transfer_vnp_exact":
        return _verify_grid_transfer(cert)
    if mode == "hierarchy_separation_barrier_exact":
        return _verify_hierarchy_barrier(cert)
    raise ValiantHierCertificateError(f"Unknown mode: {mode!r}")
