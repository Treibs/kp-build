---
id: table-key-by-value-green
statement: '`sui::table` functions take the key BY VALUE, not by reference: `table.contains(key)`
  / `table.borrow(key)` with `K: copy + drop + store`. Pass the `String` (or other
  key) itself — key types are copyable, so passing by value is cheap and correct.'
paper: ''
supporting_passage: sui 1.74.1 builds a module calling `names.contains(name)` with
  a `String` key passed by value against `&Table<String, address>`, with exit 0 and
  zero warnings.
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
  checked: '2026-07-09'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/table-key-by-value-green
grounding: {}
judgment: {}
---

`sui::table` functions take the key BY VALUE, not by reference: `table.contains(key)` / `table.borrow(key)` with `K: copy + drop + store`. Pass the `String` (or other key) itself — key types are copyable, so passing by value is cheap and correct.

> sui 1.74.1 builds a module calling `names.contains(name)` with a `String` key passed by value against `&Table<String, address>`, with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
