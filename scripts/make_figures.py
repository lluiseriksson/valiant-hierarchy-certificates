"""Generate 3 publication-quality 300-DPI figures for Paper 20.
Author: Lluis Eriksson
"""
from __future__ import annotations

import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIG_DIR = ROOT / "paper" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9.5,
    "axes.titlesize": 10.0,
    "axes.labelsize": 9.2,
    "legend.fontsize": 7.5,
    "xtick.labelsize": 8.4,
    "ytick.labelsize": 8.4,
    "axes.grid": True,
    "grid.alpha": 0.28,
    "grid.linestyle": "--",
})


def make_fig1() -> None:
    d4 = json.loads((RESULTS / "exp4_hierarchy_exponents.json").read_text(encoding="utf-8"))
    d3 = json.loads((RESULTS / "exp3_grid_transfer_scaling.json").read_text(encoding="utf-8"))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.65), dpi=300)

    # Panel (a): OpenAI Theorem 1.1 superpolynomial exponents vs fixed polynomial degree
    r4 = d4["rows"]
    xs = [r["log2_n"] for r in r4]
    ax1.plot(xs, [r["path_formula_exp"] for r in r4], "o-", color="#1b6ca8", lw=2.1, ms=5.5,
             label=r"Path formula exponent: $\ln\ln n$")
    ax1.plot(xs, [r["tree_abp_exp"] for r in r4], "s--", color="#2a9d8f", lw=2.0, ms=5.5,
             label=r"Tree ABP exponent: $\sqrt{\ln\ln n}$")
    ax1.plot(xs, [r["grid_circuit_exp"] for r in r4], "^-.", color="#c1121f", lw=2.0, ms=5.8,
             label=r"Grid circuit exponent: $(\ln n)^{1/12}$")
    ax1.axhline(2.0, color="#666", lw=1.3, ls=":", label=r"Reference degree $k=2$")
    ax1.set_xscale("log", base=2)
    ax1.set_xticks(xs)
    ax1.set_xticklabels([str(x) for x in xs])
    ax1.set_xlabel(r"Problem scale $\log_2 n$")
    ax1.set_ylabel(r"Reference exponent $e(n)$ in $n^{e(n)}$")
    ax1.set_title(r"(a) Reference Hierarchy Exponents [4]")
    ax1.legend(loc="upper left", frameon=True, framealpha=0.94)

    # Panel (b): Square grid exact transfer-matrix contraction vs brute-force state space (q=2)
    r3 = d3["rows"]
    ns = [r["grid_n"] for r in r3]
    l1 = ax2.semilogy(ns, [r["brute_force_states"] for r in r3], "s--", color="#c1121f", lw=2.0, ms=5.8,
                      label=r"Brute-force edge states $2^{2n(n-1)}$")
    l2 = ax2.semilogy(ns, [r["frontier_dim"] for r in r3], "o-", color="#1b6ca8", lw=2.1, ms=5.8,
                      label=r"Transfer frontier dim $2^n$")
    ax2.set_xticks(ns)
    ax2.set_xticklabels([f"{n}x{n}" for n in ns])
    ax2.set_xlabel(r"Square grid dimensions $n \times n$ ($q=2$)")
    ax2.set_ylabel(r"State space dimension (log scale)")
    ax2.set_title(r"(b) Grid $\mathsf{VNP}$ State Space vs. Transfer Frontier")
    ax2.legend(loc="upper left", frameon=True, framealpha=0.94)

    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig1_hierarchy_and_grid.png", dpi=300)
    plt.close(fig)


def make_fig2() -> None:
    d2 = json.loads((RESULTS / "exp2_path_and_tree_scaling.json").read_text(encoding="utf-8"))
    d3 = json.loads((RESULTS / "exp3_grid_transfer_scaling.json").read_text(encoding="utf-8"))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.65), dpi=300)

    # Panel (a): Exact-Q Path (ABP/Bisection) vs Binary Tree (VP Circuit DP) verification latency (q=3)
    r2 = d2["rows"]
    vs = [r["vertices"] for r in r2]
    ax1.plot(vs, [r["path_verify_ms"] for r in r2], "o-", color="#1b6ca8", lw=2.1, ms=5.8,
             label=r"Path $Z_{P_d,3}$ (ABP + bisection)")
    ax1.plot(vs, [r["tree_verify_ms"] for r in r2], "s--", color="#2a9d8f", lw=2.1, ms=5.8,
             label=r"Binary tree $Z_{T_L,3}$ (bottom-up $\mathsf{VP}$ DP)")
    ax1.set_xticks(vs)
    ax1.set_xlabel(r"Matched graph vertex count $|V| = 2^L - 1$ ($q=3$)")
    ax1.set_ylabel(r"Exact-$\mathbb{Q}$ verification latency (ms)")
    ax1.set_title(r"(a) Polynomial Path ($\mathsf{VBP}$) vs. Tree ($\mathsf{VP}$) Replay")
    ax1.legend(loc="upper left", frameon=True, framealpha=0.94)

    # Panel (b): Square grid exact transfer-matrix replay latency (2x2 to 5x5, q=2)
    r3 = d3["rows"]
    ns = [r["grid_n"] for r in r3]
    ax2.semilogy(ns, [max(0.01, r["verify_ms"]) for r in r3], "^-", color="#c1121f", lw=2.2, ms=6.2,
                 label=r"Exact-$\mathbb{Q}$ transfer DP latency (ms)")
    for n, r in zip(ns, r3):
        ax2.text(n, r["verify_ms"] * 1.25, f"{r['verify_ms']:.2f} ms", ha="center", va="bottom", fontsize=7.6)
    ax2.set_xticks(ns)
    ax2.set_xticklabels([f"{n}x{n}" for n in ns])
    ax2.set_xlim(1.72, 5.28)
    ax2.set_ylim(0.05, max(r["verify_ms"] for r in r3) * 3.0)
    ax2.set_xlabel(r"Square grid $n \times n$ ($E = 2n(n-1)$ edges, $q=2$)")
    ax2.set_ylabel(r"Exact-$\mathbb{Q}$ replay latency (ms, log scale)")
    ax2.set_title(r"(b) Exponential Treewidth Cost on Grids ($\mathsf{VNP}$)")
    ax2.legend(loc="upper left", frameon=True, framealpha=0.94)

    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig2_model_replay_scaling.png", dpi=300)
    plt.close(fig)


def make_fig3() -> None:
    d1 = json.loads((RESULTS / "exp1_certified_atlas.json").read_text(encoding="utf-8"))
    rows = d1["rows"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.9), dpi=300, gridspec_kw={"width_ratios": [1.55, 1.0]})

    mode_colors = {
        "path_abp_vs_bisection_exact": "#1b6ca8",
        "binary_tree_circuit_dp_exact": "#2a9d8f",
        "grid_transfer_vnp_exact": "#e07a5f",
        "hierarchy_separation_barrier_exact": "#c1121f",
    }
    labels = [r["file"].replace(".cert.json", "") for r in rows]
    ms = [r["verify_ms"] for r in rows]
    cols = [mode_colors[r["mode"]] for r in rows]
    y = np.arange(len(rows))
    ax1.barh(y, ms, color=cols, edgecolor="#222", lw=0.6, height=0.68)
    ax1.set_yticks(y)
    ax1.set_yticklabels(labels, fontsize=6.9)
    ax1.invert_yaxis()
    ax1.set_xlabel(r"Exact-$\mathbb{Q}$ verification latency (ms)")
    ax1.set_title(r"(a) Zero-Float Replay Latency Across 16 Certificates")

    counts = [
        sum(1 for r in rows if r["mode"] == "path_abp_vs_bisection_exact"),
        sum(1 for r in rows if r["mode"] == "binary_tree_circuit_dp_exact"),
        sum(1 for r in rows if r["mode"] == "grid_transfer_vnp_exact"),
        sum(1 for r in rows if r["mode"] == "hierarchy_separation_barrier_exact"),
    ]
    m_labels = ["Mode 1\nPath\nVBP/VF", "Mode 2\nTree\nVP/VBP", "Mode 3\nGrid\nVNP/VP", "Mode 4\nHier.\nBarrier"]
    bars = ax2.bar(range(4), counts, color=["#1b6ca8", "#2a9d8f", "#e07a5f", "#c1121f"], edgecolor="#222", lw=0.7)
    for b, c in zip(bars, counts):
        ax2.text(b.get_x() + b.get_width() / 2.0, c + 0.15, str(c), ha="center", va="bottom", fontweight="bold", fontsize=8.5)
    ax2.set_xticks(range(4))
    ax2.set_xticklabels(m_labels, fontsize=7.8)
    ax2.set_ylabel("Certified instances")
    ax2.set_ylim(0, 5.4)
    ax2.set_title("(b) Coverage Across All 4 Modes")

    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig3_atlas_summary.png", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    make_fig1()
    make_fig2()
    make_fig3()
    print("[PASS] Generated all 3 publication figures in paper/figures/.")
