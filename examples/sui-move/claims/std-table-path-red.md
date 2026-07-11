---
id: std-table-path-red
statement: 'There is no `std::table`: `use std::table::{Self, Table};` fails on sui
  1.74.1 with error[E03002] — "Unbound module: ''std::table''" (and cascades into
  unbound-type errors at every `Table` use). The std-vs-sui split is per-module: `std::string`
  is real, `std::table` is not — Table is a Sui object-system container.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects use std::table with exit 1, error[E03002],
  Unbound module: ''std::table''.'
claim_type: finding
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
  evidence: sui-move-build:red_violation cleared
  checked: '2026-07-10'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/std-table-path-red
grounding: {}
judgment: {}
---

There is no `std::table`: `use std::table::{Self, Table};` fails on sui 1.74.1 with error[E03002] — "Unbound module: 'std::table'" (and cascades into unbound-type errors at every `Table` use). The std-vs-sui split is per-module: `std::string` is real, `std::table` is not — Table is a Sui object-system container.

> sui 1.74.1 rejects use std::table with exit 1, error[E03002], Unbound module: 'std::table'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
