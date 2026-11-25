# Exact-Q Path, Binary-Tree, and Square-Grid State-Sum Certificates for Valiant's Arithmetic Hierarchy

**Author:** Lluis Eriksson (with AI-assisted formal verification, code generation, and drafting via Google Antigravity)  
**License:** MIT (code, Lean 4 proofs, certificates) / CC-BY-4.0 (manuscript)

## Overview
Inspired by OpenAI's November 24, 2026 separation of Valiant's entire arithmetic hierarchy (*Paths, trees and grids separate Valiant's hierarchy*, `openai/math`), this repository provides:
- **Zero-Dependency Lean 4 Kernel (`lean/ValiantHierarchy.lean`, Lean `v4.35.0`)**: 18 theorems with **0 warnings**, **0 `sorry`**, and **0 `Classical.choice`** (including 2 zero-axiom theorems) mechanizing exact path ABP vs. bisection state-sum equivalence, 8-term binary-tree bottom-up $\mathsf{VP}$ DP factorization, 16-term $2\times 2$ grid transfer-matrix trace equivalence, grid vertex table degree bounds ($q^d \le q^4$), multilinearity, disjoint-union multiplicativity, inductive ABP ($L q^2$) and tree-circuit ($V q^3$) budgets, exponential grid frontier growth ($q^{n+1} > q^n$), characteristic-free 1/2-bit Boolean $\mathsf{VNP}$ selectors over $\mathbb{Z}$, signed 2-path determinant embedding, strict superpolynomial hierarchy chains, and exact grid-edge/binary-tree vertex recurrences.
- **Pure-Stdlib Zero-Float Verifier (`src/valiant_certifier.py`, `VALIANT-HIER-CERT-1.0`)**: Independently replays 16 exact-$\mathbb{Q}$ certificates across all four modes in `0.049`–`4.319 ms` (contracting $5\times 5$ grids over $2^{40}$ edge states in `4.806 ms`), cross-checks all three exact evaluators against brute-force $q^E$ summation, and rejects **54/54** live adversarial red-team attacks.

## Reproduce Everything
```bash
python scripts/run_all_experiments.py
python scripts/make_figures.py
python scripts/verify_all.py
```
