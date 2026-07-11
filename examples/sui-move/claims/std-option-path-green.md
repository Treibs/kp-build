---
id: std-option-path-green
statement: '`Option<T>`/`option` are implicit `std::option` aliases in edition 2024
  — no `use` line is needed, and any explicit path is `std::option`, never `sui::`.'
paper: ''
supporting_passage: sui 1.74.1 builds a slot module using Option<address>/option::none
  with no option import, exit 0, zero warnings.
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
  artifact: sui-move-fixtures/std-option-path-green
grounding: {}
judgment: {}
---

`Option<T>`/`option` are implicit `std::option` aliases in edition 2024 — no `use` line is needed, and any explicit path is `std::option`, never `sui::`.

> sui 1.74.1 builds a slot module using Option<address>/option::none with no option import, exit 0, zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
