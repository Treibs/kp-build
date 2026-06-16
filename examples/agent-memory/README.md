# Memory for LLM Agents — persistent / long-term memory architectures for autonomous agents (2023–2026)

*wikillm knowledge package (`@kp/memory-for-llm-agents-persistent-long-term-memory`) — a research-landscape foundation.*

**Scope:** Persistent and long-term memory for autonomous LLM agents from 2023 to 2026. Covers: (a) foundational architectures (OS-style virtual context, memory streams, episodic buffers); (b) the episodic-vs-semantic memory distinction and how each is instantiated; (c) memory consolidation, updating, and forgetting (Ebbinghaus curves, ADD/UPDATE/DELETE operators, parametric self-update); (d) retrieval mechanisms (vector RAG, knowledge-graph / hippocampal indexing, temporal KGs); (e) the long-context-vs-RAG-vs-explicit-memory debate (cost vs accuracy, routing); and (f) evaluation/benchmarks for long-term interactive memory. Excludes pure long-context modeling (positional encodings, attention efficiency) except where it bears directly on the memory debate, and excludes general RAG retrieval research not framed as agent memory.

- 21/21 citations verified (arXiv/Crossref); source years 2023–2026
- 35 claims · 8 open problems · 4 debates · 0 benchmarks
- dropped (unverified-anchored): {'claims': 0, 'open_problems': 0, 'debates': 0, 'benchmarks': 0, 'positions': 0}

**Load `CONTEXT.md` into your agent** to inherit this field without re-running the research. `index.json` is the machine-readable graph (nodes + edges); the subdirectories hold the notes.

## Distribution

This is a [0xLT/kpm](https://github.com/0xLT/kpm) knowledge package (`knowledge.json`). Publish it as a tagged GitHub repo, then any consumer installs it with kpm — no re-research:

```bash
kpm add github:<owner>/<repo>#v0.1.0
kpm compose            # composes into a vault; load CONTEXT.md into your agent
```

Confidence is corpus-relative (conditional on the cited sources). Built 2026-06-15.
