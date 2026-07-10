---
id: sui-import-green
statement: The `SUI` coin type is imported from the `sui::sui` module — `use sui::sui::SUI;`
  alongside `use sui::coin::{Self, Coin};` — even though it is only ever used through
  `Coin<SUI>`/`Balance<SUI>`.
paper: ''
supporting_passage: sui 1.74.1 builds a module importing `use sui::sui::SUI` with
  Coin/Balance handling, exit 0, zero warnings.
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
  artifact: sui-move-fixtures/sui-import-green
grounding: {}
judgment: {}
---

The `SUI` coin type is imported from the `sui::sui` module — `use sui::sui::SUI;` alongside `use sui::coin::{Self, Coin};` — even though it is only ever used through `Coin<SUI>`/`Balance<SUI>`.

> sui 1.74.1 builds a module importing `use sui::sui::SUI` with Coin/Balance handling, exit 0, zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
