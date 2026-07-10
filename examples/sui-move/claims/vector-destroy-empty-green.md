---
id: vector-destroy-empty-green
statement: A drained `vector<T>` where `T` lacks `drop` is consumed explicitly with
  `vector::destroy_empty(v)` after the drain loop.
paper: ''
supporting_passage: sui 1.74.1 builds a launch_all that pops every element and then
  vector::destroy_empty's the vector, exit 0, zero warnings.
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
  artifact: sui-move-fixtures/vector-destroy-empty-green
grounding: {}
judgment: {}
---

A drained `vector<T>` where `T` lacks `drop` is consumed explicitly with `vector::destroy_empty(v)` after the drain loop.

> sui 1.74.1 builds a launch_all that pops every element and then vector::destroy_empty's the vector, exit 0, zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
