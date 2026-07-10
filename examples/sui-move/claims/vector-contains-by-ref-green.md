---
id: vector-contains-by-ref-green
statement: '`vector::contains` takes the probe element by reference: `vector::contains(blocklist,
  &who)` builds green.'
paper: ''
supporting_passage: sui 1.74.1 builds a blocked() using vector::contains(blocklist,
  &who), exit 0, zero warnings.
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
  artifact: sui-move-fixtures/vector-contains-by-ref-green
grounding: {}
judgment: {}
---

`vector::contains` takes the probe element by reference: `vector::contains(blocklist, &who)` builds green.

> sui 1.74.1 builds a blocked() using vector::contains(blocklist, &who), exit 0, zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
