---
id: object-new-green
statement: 'Create object UIDs only with `object::new(ctx)`, which takes `&mut TxContext`
  and returns a fresh `UID`: `Item { id: object::new(ctx), ... }`.'
paper: ''
supporting_passage: sui 1.74.1 builds an object constructor that mints its UID via
  `object::new(ctx)` with exit 0.
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
  checked: '2026-07-08'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/object-new-green
grounding: {}
judgment: {}
---

Create object UIDs only with `object::new(ctx)`, which takes `&mut TxContext` and returns a fresh `UID`: `Item { id: object::new(ctx), ... }`.

> sui 1.74.1 builds an object constructor that mints its UID via `object::new(ctx)` with exit 0.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
