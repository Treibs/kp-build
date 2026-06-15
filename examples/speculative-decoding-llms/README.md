# Speculative Decoding for Fast LLM Inference: Draft-then-Verify Acceleration with Lossless Guarantees

*wikillm knowledge package (`@kp/speculative-decoding-for-fast-llm-inference-draft-then`) — a research-landscape foundation.*

**Scope:** IN SCOPE: lossless (or controllably-lossy) inference-acceleration methods for autoregressive LLM decoding that use a cheap "draft" proposal verified in parallel by the target model, including speculative sampling, self-speculative / layer-skip drafting, feature-level autoregression (Medusa, EAGLE/EAGLE-2/EAGLE-3), parallel/Jacobi and Lookahead decoding, and tree-structured/multi-candidate verification (SpecInfer); the analysis covers acceptance-rate theory, the distribution-preservation (losslessness) guarantee, wall-clock speedup vs. memory/compute trade-offs, and draft-model training/alignment. OUT OF SCOPE: orthogonal efficiency techniques (quantization, pruning, distillation as a standalone goal, KV-cache compression, FlashAttention-style kernels, MoE routing, continuous batching/PagedAttention) except where they directly interact with or are composed with speculative decoding; and non-autoregressive paradigms (diffusion LMs) that replace rather than accelerate AR decoding. Emphasis is on the 2024-2026 frontier (EAGLE-2/3, dynamic-tree and online drafting, long-context/reasoning/batched-serving regimes) over pre-2024 foundations.

- 17/17 citations verified (arXiv/Crossref); source years 2023–2026
- 37 claims · 6 open problems · 2 debates · 17 benchmarks
- dropped (unverified-anchored): {'claims': 0, 'open_problems': 0, 'debates': 0, 'benchmarks': 0, 'positions': 0}

**Load `CONTEXT.md` into your agent** to inherit this field without re-running the research. `index.json` is the machine-readable graph (nodes + edges); the subdirectories hold the notes.

## Distribution

This is a [0xLT/kpm](https://github.com/0xLT/kpm) knowledge package (`knowledge.json`). Publish it as a tagged GitHub repo, then any consumer installs it with kpm — no re-research:

```bash
kpm add github:<owner>/<repo>#v0.1.0
kpm compose            # composes into a vault; load CONTEXT.md into your agent
```

Confidence is corpus-relative (conditional on the cited sources). Built 2026-06-15.
