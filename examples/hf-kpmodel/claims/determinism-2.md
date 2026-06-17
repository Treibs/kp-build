---
id: determinism-2
statement: Never use Date.now(), new Date(), performance.now(), or any wall-clock
  / time-based logic in a composition script; pin content and per-frame behaviour
  to the GSAP timeline position so the render is identical across runs.
paper: ''
supporting_passage: '**Deterministic:** No `Math.random()`, `Date.now()`, or time-based
  logic. Use a seeded PRNG if you need pseudo-random values (e.g. mulberry32).'
claim_type: method
confidence: high
corroborated_by: []
survived_refuter: true
grounded: unchecked
verified:
  exists: true
  status: verified
  kind: execution
  via: lint
  canonical_title: ''
  match_score: 0.0
  evidence: lint:non_deterministic_code cleared
  checked: '2026-06-17'
execution:
  tool: lint
  gate_code: non_deterministic_code
  artifact: hf-kpmodel-fixtures/determinism-2
---

Never use Date.now(), new Date(), performance.now(), or any wall-clock / time-based logic in a composition script; pin content and per-frame behaviour to the GSAP timeline position so the render is identical across runs.

> **Deterministic:** No `Math.random()`, `Date.now()`, or time-based logic. Use a seeded PRNG if you need pseudo-random values (e.g. mulberry32).

— *execution verified* via lint: lint:non_deterministic_code cleared
