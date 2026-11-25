"""Gate-2 verification, brute-force q^E cross-checks, and 54-attack live red-team suite for Paper 20.
Author: Lluis Eriksson
"""
from __future__ import annotations

import copy
import itertools
import json
import pathlib
import sys
from decimal import Decimal
from fractions import Fraction

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.valiant_certifier import ValiantHierCertificateError, verify_valiant_hier_certificate_exact
from src.valiant_exact import (
    binary_tree_state_sum_dp_exact,
    grid_state_sum_transfer_exact,
    path_state_sum_abp_exact,
    path_state_sum_bisection_exact,
)

CERTS_DIR = ROOT / "results" / "certificates"


def _brute_force_path(lv, mats, rv) -> Fraction:
    q = len(lv)
    n_edges = len(mats) + 1
    total = Fraction(0, 1)
    for assign in itertools.product(range(q), repeat=n_edges):
        w = lv[assign[0]] * rv[assign[-1]]
        for t, M in enumerate(mats):
            w *= M[assign[t]][assign[t + 1]]
        total += w
    return total


def _brute_force_grid(rows: int, cols: int, q: int, tables) -> Fraction:
    edges = []
    for r in range(rows):
        for c in range(cols):
            if r < rows - 1:
                edges.append(("V", r, c))
            if c < cols - 1:
                edges.append(("H", r, c))
    e_idx = {e: i for i, e in enumerate(edges)}
    total = Fraction(0, 1)
    for assign in itertools.product(range(q), repeat=len(edges)):
        w = Fraction(1, 1)
        for r in range(rows):
            for c in range(cols):
                inc = []
                if r > 0:
                    inc.append(("V", r - 1, c))
                if c > 0:
                    inc.append(("H", r, c - 1))
                if r < rows - 1:
                    inc.append(("V", r, c))
                if c < cols - 1:
                    inc.append(("H", r, c))
                t_idx = 0
                for e in inc:
                    t_idx = t_idx * q + assign[e_idx[e]]
                w *= tables[(r, c)][t_idx]
        total += w
    return total


def test_exact_evaluators_match_brute_force_state_sums() -> None:
    """Independently cross-check ABP, bisection, binary-tree DP, and grid transfer DP against brute-force q^E."""
    # Path d=5, q=2 (2^4 = 16 edge states)
    lv = [Fraction(1, 2), Fraction(-3, 1)]
    rv = [Fraction(2, 1), Fraction(5, 2)]
    mats = [
        [[Fraction(1), Fraction(-2)], [Fraction(3, 2), Fraction(1)]],
        [[Fraction(-1, 2), Fraction(4)], [Fraction(2), Fraction(-3)]],
        [[Fraction(3), Fraction(1, 2)], [Fraction(-1), Fraction(2)]],
    ]
    bf_p = _brute_force_path(lv, mats, rv)
    assert path_state_sum_abp_exact(lv, mats, rv) == bf_p
    assert path_state_sum_bisection_exact(lv, mats, rv) == bf_p

    # Binary tree L=2, q=2 (empty internal_tensors) & L=3, q=2 (64 edge states)
    leaves2 = [[Fraction(2), Fraction(-1)], [Fraction(3), Fraction(5)]]
    root2 = [[Fraction(1), Fraction(-2)], [Fraction(4), Fraction(3)]]
    bf_t2 = sum(leaves2[0][a] * leaves2[1][b] * root2[a][b] for a in range(2) for b in range(2))
    assert binary_tree_state_sum_dp_exact(2, 2, leaves2, [], root2) == bf_t2

    leaves = [[Fraction(1), Fraction(-2)], [Fraction(3), Fraction(1, 2)], [Fraction(-1), Fraction(2)], [Fraction(2), Fraction(-1, 2)]]
    tL = [[[Fraction(a - b + c + 1, 2) for c in range(2)] for b in range(2)] for a in range(2)]
    tR = [[[Fraction(2 * a + b - c, 1) for c in range(2)] for b in range(2)] for a in range(2)]
    root_m = [[Fraction(1), Fraction(-3)], [Fraction(2), Fraction(5)]]
    bf_t = Fraction(0, 1)
    for e0, e1, e2, e3, eL, eR in itertools.product(range(2), repeat=6):
        bf_t += leaves[0][e0] * leaves[1][e1] * tL[e0][e1][eL] * leaves[2][e2] * leaves[3][e3] * tR[e2][e3][eR] * root_m[eL][eR]
    assert binary_tree_state_sum_dp_exact(3, 2, leaves, [tL, tR], root_m) == bf_t

    # Grid 2x3 (128 states) and Grid 3x3 (4096 states, covering degree-4 interior vertex (1,1))
    for rows, cols in ((2, 3), (3, 3)):
        tables = {}
        for r in range(rows):
            for c in range(cols):
                deg = int(r > 0) + int(c > 0) + int(r < rows - 1) + int(c < cols - 1)
                tables[(r, c)] = [Fraction(((r * 7 + c * 5 + i * 3) % 5) - 2, 1) for i in range(2 ** deg)]
        assert grid_state_sum_transfer_exact(rows, cols, 2, tables) == _brute_force_grid(rows, cols, 2, tables)


def test_all_16_certificates_verify_cleanly() -> None:
    files = sorted(CERTS_DIR.glob("*.cert.json"))
    assert len(files) == 16
    for f in files:
        res = verify_valiant_hier_certificate_exact(json.loads(f.read_text(encoding="utf-8")))
        assert res["verified"] is True


def test_54_live_adversarial_red_team_attacks_rejected() -> None:
    c1 = json.loads((CERTS_DIR / "path_d4_q2.cert.json").read_text(encoding="utf-8"))
    c2 = json.loads((CERTS_DIR / "tree_L3_q2.cert.json").read_text(encoding="utf-8"))
    c3 = json.loads((CERTS_DIR / "grid_2x2_q2.cert.json").read_text(encoding="utf-8"))
    c4 = json.loads((CERTS_DIR / "hier_barrier_n4.cert.json").read_text(encoding="utf-8"))

    attacks = []

    def add(name, base, fn):
        cand = copy.deepcopy(base)
        fn(cand)
        attacks.append((name, cand))

    # Group A: Schema, Types & Canonical Rationals (16 attacks)
    attacks.append(("01_root_not_dict", ["bad"]))
    add("02_wrong_schema", c1, lambda x: x.__setitem__("schema", "VALIANT-HIER-CERT-9.9"))
    add("03_unknown_mode", c1, lambda x: x.__setitem__("mode", "bogus"))
    add("04_extra_key", c1, lambda x: x.__setitem__("evil", 1))
    add("05_missing_key", c1, lambda x: x.pop("matrices"))
    add("06_float_injection", c1, lambda x: x["left_vec"].__setitem__(0, 0.5))
    add("07_bool_injection", c1, lambda x: x.__setitem__("states_q", True))
    add("08_decimal_injection", c1, lambda x: x["left_vec"].__setitem__(0, Decimal("0.5")))
    add("09_complex_injection", c1, lambda x: x["left_vec"].__setitem__(0, 1 + 0j))
    add("10_tuple_injection", c1, lambda x: x.__setitem__("left_vec", tuple(x["left_vec"])))
    add("11_non_str_key", c1, lambda x: x.__setitem__(99, "bad"))
    add("12_unreduced_frac", c1, lambda x: x["left_vec"].__setitem__(0, "2/4"))
    add("13_denom_one_frac", c1, lambda x: x["left_vec"].__setitem__(0, "1/1"))
    add("14_neg_zero", c1, lambda x: x["left_vec"].__setitem__(0, "-0"))
    add("15_non_str_name", c1, lambda x: x.__setitem__("name", 99))
    add("16_empty_name", c1, lambda x: x.__setitem__("name", "  "))

    # Group B: Mode 1 Path ABP vs Bisection Forgeries (10 attacks)
    add("17_path_d_below_3", c1, lambda x: x.__setitem__("num_vertices_d", 2))
    add("18_path_q_below_2", c1, lambda x: x.__setitem__("states_q", 1))
    add("19_path_wrong_mat_count", c1, lambda x: x["matrices"].pop())
    add("20_path_wrong_left_len", c1, lambda x: x["left_vec"].pop())
    add("21_path_wrong_right_len", c1, lambda x: x["right_vec"].pop())
    add("22_path_wrong_mat_shape", c1, lambda x: x["matrices"][0].pop())
    add("23_path_forged_state_sum", c1, lambda x: x.__setitem__("claimed_state_sum", "999999"))
    add("24_path_tampered_entry", c1, lambda x: x["matrices"][0][0].__setitem__(0, "999"))
    add("25_path_d_above_max", c1, lambda x: x.__setitem__("num_vertices_d", 99))
    add("26_path_q_above_max", c1, lambda x: x.__setitem__("states_q", 99))

    # Group C: Mode 2 Binary Tree VP Circuit DP Forgeries (10 attacks)
    add("27_tree_L_below_2", c2, lambda x: x.__setitem__("levels_L", 1))
    add("28_tree_L_above_max", c2, lambda x: x.__setitem__("levels_L", 9))
    add("29_tree_q_below_2", c2, lambda x: x.__setitem__("states_q", 1))
    add("30_tree_wrong_leaf_count", c2, lambda x: x["leaf_vecs"].pop())
    add("31_tree_wrong_int_count", c2, lambda x: x["internal_tensors"].pop())
    add("32_tree_wrong_root_shape", c2, lambda x: x["root_mat"].pop())
    add("33_tree_forged_state_sum", c2, lambda x: x.__setitem__("claimed_state_sum", "999999"))
    add("34_tree_tampered_leaf", c2, lambda x: x["leaf_vecs"][0].__setitem__(0, "999"))
    add("35_tree_tampered_internal", c2, lambda x: x["internal_tensors"][0][1][1].__setitem__(1, "999"))
    add("36_tree_tampered_root", c2, lambda x: x["root_mat"][0].__setitem__(0, "999"))

    # Group D: Mode 3 Square Grid Transfer VNP Forgeries (9 attacks)
    add("37_grid_rows_below_2", c3, lambda x: x.__setitem__("rows", 1))
    add("38_grid_cols_below_2", c3, lambda x: x.__setitem__("cols", 1))
    add("39_grid_q_below_2", c3, lambda x: x.__setitem__("states_q", 1))
    add("40_grid_missing_vertex", c3, lambda x: x["vertex_tables"].pop("0,0"))
    add("41_grid_extra_vertex", c3, lambda x: x["vertex_tables"].__setitem__("9,9", ["1", "1", "1", "1"]))
    add("42_grid_wrong_table_len", c3, lambda x: x["vertex_tables"]["0,0"].pop())
    add("43_grid_forged_state_sum", c3, lambda x: x.__setitem__("claimed_state_sum", "999999"))
    add("44_grid_tampered_table_val", c3, lambda x: x["vertex_tables"]["0,0"].__setitem__(0, "999"))
    add("45_grid_q_above_max", c3, lambda x: x.__setitem__("states_q", 9))

    # Group E: Mode 4 Hierarchy Separation Barrier Forgeries (9 attacks)
    add("46_selector_wrong_len", c4, lambda x: x["selector_table"].pop())
    add("47_grid_n_below_2", c4, lambda x: x.__setitem__("grid_n", 1))
    add("48_tree_L_below_2_m4", c4, lambda x: x.__setitem__("tree_levels_L", 1))
    add("49_base_n_below_2", c4, lambda x: x.__setitem__("base_n", 1))
    add("50_poly_k_zero", c4, lambda x: x.__setitem__("poly_exp_k", 0))
    add("51_s1_not_gt_k", c4, lambda x: x.__setitem__("exp_s1_vf", x["poly_exp_k"]))
    add("52_s2_not_gt_s1", c4, lambda x: x.__setitem__("exp_s2_vbp", x["exp_s1_vf"]))
    add("53_s3_not_gt_s2", c4, lambda x: x.__setitem__("exp_s3_vp", x["exp_s2_vbp"]))
    add("54_s3_above_max", c4, lambda x: x.__setitem__("exp_s3_vp", 99))

    assert len(attacks) == 54
    for name, cand in attacks:
        with pytest.raises(ValiantHierCertificateError):
            verify_valiant_hier_certificate_exact(cand)
