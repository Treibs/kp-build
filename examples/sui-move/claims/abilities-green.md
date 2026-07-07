---
id: abilities-green
statement: 'A struct with the `key` ability must have `id: UID` as its first field:
  `public struct Item has key { id: UID, value: u64 }`, with the UID created by `object::new(ctx)`.'
paper: ''
supporting_passage: 'sui 1.74.1 builds a `key` struct whose first field is `id: UID`
  (initialized with `object::new(ctx)`) with exit 0.'
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
  checked: '2026-07-07'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/abilities-green
grounding: {}
judgment: {}
---

A struct with the `key` ability must have `id: UID` as its first field: `public struct Item has key { id: UID, value: u64 }`, with the UID created by `object::new(ctx)`.

> sui 1.74.1 builds a `key` struct whose first field is `id: UID` (initialized with `object::new(ctx)`) with exit 0.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
