---
id: compound-assignment-green
statement: Accumulation is written out in full — `t.total = t.total + n` — there is
  no compound-assignment shorthand in Move; the written-out form builds green.
paper: ''
supporting_passage: sui 1.74.1 builds a module accumulating with the written-out `t.total
  = t.total + n` form, with exit 0 and zero warnings.
claim_type: method
confidence: high
corroborated_by: []
survived_refuter: true
grounded: unchecked
verified:
  exists: true
  status: verified
  kind: execution
  via: sui-move-build
  canonical_title: ''
  match_score: 0.0
  evidence: sui-move-build:build_error cleared
  checked: '2026-07-10'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/compound-assignment-green
grounding: {}
judgment: {}
---

Accumulation is written out in full — `t.total = t.total + n` — there is no compound-assignment shorthand in Move; the written-out form builds green.

> sui 1.74.1 builds a module accumulating with the written-out `t.total = t.total + n` form, with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
