---
id: std-table-path-green
statement: '`Table` imports from the Sui framework: `use sui::table::{Self, Table};`
  — constructed with `table::new(ctx)` and stored as an object field.'
paper: ''
supporting_passage: sui 1.74.1 builds a registry module importing sui::table with
  table::new/length, exit 0, zero warnings.
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
  artifact: sui-move-fixtures/std-table-path-green
grounding: {}
judgment: {}
---

`Table` imports from the Sui framework: `use sui::table::{Self, Table};` — constructed with `table::new(ctx)` and stored as an object field.

> sui 1.74.1 builds a registry module importing sui::table with table::new/length, exit 0, zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
