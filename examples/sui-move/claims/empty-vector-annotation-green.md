---
id: empty-vector-annotation-green
statement: 'An empty vector with no downstream element-type evidence states its type
  at creation: `let owners = vector<address>[];` (the typed literal) builds green.'
paper: ''
supporting_passage: sui 1.74.1 builds a function creating vector<address>[] and taking
  its length, exit 0, zero warnings.
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
  artifact: sui-move-fixtures/empty-vector-annotation-green
grounding: {}
judgment: {}
---

An empty vector with no downstream element-type evidence states its type at creation: `let owners = vector<address>[];` (the typed literal) builds green.

> sui 1.74.1 builds a function creating vector<address>[] and taking its length, exit 0, zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
