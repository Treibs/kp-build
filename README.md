# kp-build — wikillm knowledge packages

Build a **portable, citation-verified, agent-loadable** research-landscape package: the literature
foundation to *begin* a PhD-level paper on a narrow topic. Built once, shared, so nobody's agent
re-spends the compute to reconstruct the field.

- **No hallucinated citations** — every paper is checked against arXiv/Crossref; unverifiable ones drop.
- **Open-problems register** — where new work goes (mined from papers' future-work sections).
- **`CONTEXT.md`** — a token-bounded field briefing an agent loads to inherit the topic.
- **Falsification gate** — `kp_build.falsify` scores whether a KP-loaded agent beats a base agent
  (objective metric: citation hallucination rate, checked live).

See `SPEC.md` for the package format and pipeline. `pip install -e .` then `kp-build build -i research.json -o out/`.

When it pays off: topics the model is WEAK on (recent / niche / post-cutoff). For topics the model
already knows well, the package adds traceability and reuse but not accuracy — and the falsification
gate will honestly tell you so.
