# Variable-width transformer scaling (arXiv:2606.18246): nonuniform layer-width allocation

*wikillm knowledge package (`@kp/variable-width-transformer-scaling-arxiv-2606-18246-nonuniform`) — a research-landscape foundation.*

**Scope:** A doc-grounding knowledge pack on a frontier result published 2026-06-16 — past a typical model's training cutoff, so its specifics (the architecture's shape and its FLOP/KV-cache numbers) are exactly what an unaided model fabricates. Each claim's verbatim passage is checked against the paper's pinned abstract (corpus/VariableWidthTransformers.txt) by the DocGroundingVerifier (`kp-build build --ground-verify`). A claim ships only if its quoted sentence is present; an invented variant (wrong numbers, wrong direction) is stamped `ungrounded` and dropped. Provenance, not soundness: grounding proves the clause is verbatim in the abstract, not that the result replicates.

- 0/0 citations verified (arXiv/Crossref); source years n/a
- 3 claims · 0 open problems · 0 debates · 0 benchmarks
- dropped (unverified-anchored): {'claims': 1, 'open_problems': 0, 'debates': 0, 'benchmarks': 0, 'positions': 0, 'relations': 0}

**Load `CONTEXT.md` into your agent** to inherit this field without re-running the research. `index.json` is the machine-readable graph (nodes + edges); the subdirectories hold the notes.

## Distribution

This is a [0xLT/kpm](https://github.com/0xLT/kpm) knowledge package (`knowledge.json`). Publish it as a tagged GitHub repo, then any consumer installs it with kpm — no re-research:

```bash
kpm add github:<owner>/<repo>#v0.1.0
kpm compose            # composes into a vault; load CONTEXT.md into your agent
```

Confidence is corpus-relative (conditional on the cited sources). Built 2026-06-17.
