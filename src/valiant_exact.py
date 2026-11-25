"""Pure-stdlib zero-float exact-Q path, binary-tree, and square-grid state-sum evaluators.
Author: Lluis Eriksson
"""
from __future__ import annotations

from fractions import Fraction
from typing import Dict, List, Sequence, Tuple


def mat_mul_q(A: Sequence[Sequence[Fraction]], B: Sequence[Sequence[Fraction]]) -> List[List[Fraction]]:
    n = len(A)
    m = len(B[0])
    k = len(B)
    out = [[Fraction(0, 1)] * m for _ in range(n)]
    for i in range(n):
        for t in range(k):
            a_it = A[i][t]
            if a_it == 0:
                continue
            for j in range(m):
                out[i][j] += a_it * B[t][j]
    return out


def path_state_sum_abp_exact(
    left_vec: Sequence[Fraction],
    matrices: Sequence[Sequence[Sequence[Fraction]]],
    right_vec: Sequence[Fraction],
) -> Fraction:
    """Evaluate Z_{P_d, q} via sequential O(d q^2) Algebraic Branching Program sweep."""
    q = len(left_vec)
    cur = list(left_vec)
    for M in matrices:
        nxt = [Fraction(0, 1)] * q
        for i in range(q):
            ci = cur[i]
            if ci == 0:
                continue
            for j in range(q):
                nxt[j] += ci * M[i][j]
        cur = nxt
    return sum((cur[i] * right_vec[i] for i in range(q)), Fraction(0, 1))


def _bisect_mat_prod(mats: Sequence[Sequence[Sequence[Fraction]]]) -> List[List[Fraction]]:
    if len(mats) == 1:
        return [list(row) for row in mats[0]]
    mid = len(mats) // 2
    L = _bisect_mat_prod(mats[:mid])
    R = _bisect_mat_prod(mats[mid:])
    return mat_mul_q(L, R)


def path_state_sum_bisection_exact(
    left_vec: Sequence[Fraction],
    matrices: Sequence[Sequence[Sequence[Fraction]]],
    right_vec: Sequence[Fraction],
) -> Fraction:
    """Evaluate Z_{P_d, q} via O(log d)-depth divide-and-conquer bisection (formula model)."""
    q = len(left_vec)
    if not matrices:
        return sum((left_vec[i] * right_vec[i] for i in range(q)), Fraction(0, 1))
    P = _bisect_mat_prod(matrices)
    total = Fraction(0, 1)
    for i in range(q):
        for j in range(q):
            total += left_vec[i] * P[i][j] * right_vec[j]
    return total


def binary_tree_state_sum_dp_exact(
    levels: int,
    q: int,
    leaf_vecs: Sequence[Sequence[Fraction]],
    internal_tensors: Sequence[Sequence[Sequence[Sequence[Fraction]]]],
    root_mat: Sequence[Sequence[Fraction]],
) -> Fraction:
    """Evaluate complete binary tree Z_{T_L, q} via bottom-up VP arithmetic circuit DP.
    levels >= 2: 2^(L-1) leaves, 2^(L-1)-2 internal non-root nodes (indexed bottom-up level by level),
    and 1 root matrix R[a][b].
    """
    if levels < 2:
        raise ValueError("levels must be >= 2")
    n_leaves = 1 << (levels - 1)
    if len(leaf_vecs) != n_leaves:
        raise ValueError(f"Expected {n_leaves} leaf vectors, got {len(leaf_vecs)}")
    cur_layer: List[List[Fraction]] = [list(v) for v in leaf_vecs]
    idx = 0
    while len(cur_layer) > 2:
        nxt_layer: List[List[Fraction]] = []
        for p in range(0, len(cur_layer), 2):
            lv = cur_layer[p]
            rv = cur_layer[p + 1]
            T = internal_tensors[idx]
            idx += 1
            out = [Fraction(0, 1)] * q
            for a in range(q):
                la = lv[a]
                if la == 0:
                    continue
                for b in range(q):
                    lab = la * rv[b]
                    if lab == 0:
                        continue
                    for c in range(q):
                        out[c] += lab * T[a][b][c]
            nxt_layer.append(out)
        cur_layer = nxt_layer
    if idx != len(internal_tensors):
        raise ValueError("Unused internal_tensors remaining")
    lv, rv = cur_layer[0], cur_layer[1]
    total = Fraction(0, 1)
    for a in range(q):
        for b in range(q):
            total += lv[a] * rv[b] * root_mat[a][b]
    return total


def grid_state_sum_transfer_exact(
    rows: int,
    cols: int,
    q: int,
    vertex_tables: Dict[Tuple[int, int], List[Fraction]],
) -> Fraction:
    """Evaluate r x c grid state sum Z_{Grid_{r x c}, q} via exact boundary-frontier transfer DP.
    At each vertex (r, c), incident edges are ordered canonically as [up, left, down, right]
    (omitting edges outside the grid). Thus degree d in {2, 3, 4} and table length == q^d,
    indexed in big-endian base-q order of the incident edge labels.
    """
    if rows < 2 or cols < 2 or q < 2:
        raise ValueError("Require rows >= 2, cols >= 2, q >= 2")
    # Frontier holds horizontal edges entering current column + vertical edge from above:
    # Process vertices in column-major order: c = 0..cols-1, r = 0..rows-1.
    # Maintain frontier dict mapping tuple of active edge labels -> accumulated Fraction weight.
    # Active edges at step (r, c):
    #   - horizontal edges (i, c-1)->(i, c) for i >= r (if c > 0)
    #   - horizontal edges (i, c)->(i, c+1) for i < r (if c < cols - 1)
    #   - vertical edge (r-1, c)->(r, c) (if r > 0)
    # Even simpler and 100% explicit: represent frontier as dict[tuple[tuple[str,int,int], ...], Fraction]
    # keyed by canonical edge IDs; since vertices are processed in fixed column-major order,
    # the active edge tuple has size <= rows + 1 at every step!
    active_edges: List[Tuple[str, int, int]] = []
    dp: Dict[Tuple[int, ...], Fraction] = {(): Fraction(1, 1)}

    for c in range(cols):
        for r in range(rows):
            # Canonical incident edges [up, left, down, right] that exist in grid
            inc: List[Tuple[str, int, int]] = []
            if r > 0:
                inc.append(("V", r - 1, c))
            if c > 0:
                inc.append(("H", r, c - 1))
            if r < rows - 1:
                inc.append(("V", r, c))
            if c < cols - 1:
                inc.append(("H", r, c))

            table = vertex_tables[(r, c)]
            d = len(inc)
            if len(table) != q ** d:
                raise ValueError(f"Vertex ({r},{c}) has degree {d}, expected table len {q**d}, got {len(table)}")

            # Incoming edges are already in active_edges (and will be retired after this vertex!)
            in_edges = [e for e in inc if e in active_edges]
            out_edges = [e for e in inc if e not in active_edges]
            in_pos = {e: active_edges.index(e) for e in in_edges}
            keep_edges = [e for e in active_edges if e not in in_pos]
            keep_pos = [active_edges.index(e) for e in keep_edges]
            new_active = keep_edges + out_edges

            # Map each incident edge position in `inc` to either an incoming index or an outgoing index
            inc_is_in = [e in in_pos for e in inc]
            inc_idx = [in_pos[e] if e in in_pos else out_edges.index(e) for e in inc]

            # Enumerate all q^len(out_edges) assignments to new outgoing edges
            n_out = len(out_edges)
            out_assigns: List[Tuple[int, ...]] = [()]
            for _ in range(n_out):
                out_assigns = [a + (s,) for a in out_assigns for s in range(q)]

            nxt_dp: Dict[Tuple[int, ...], Fraction] = {}
            for state, wt in dp.items():
                if wt == 0:
                    continue
                kept = tuple(state[p] for p in keep_pos)
                for oa in out_assigns:
                    # Compute table index in big-endian base-q
                    t_idx = 0
                    for is_in, ii in zip(inc_is_in, inc_idx):
                        lbl = state[ii] if is_in else oa[ii]
                        t_idx = t_idx * q + lbl
                    tw = table[t_idx]
                    if tw == 0:
                        continue
                    ns = kept + oa
                    prev = nxt_dp.get(ns)
                    nxt_dp[ns] = wt * tw if prev is None else prev + wt * tw
            active_edges = new_active
            dp = nxt_dp

    assert active_edges == []
    return dp.get((), Fraction(0, 1))


def fmt_rat(q: Fraction) -> str:
    if q.denominator == 1:
        return str(q.numerator)
    return f"{q.numerator}/{q.denominator}"
