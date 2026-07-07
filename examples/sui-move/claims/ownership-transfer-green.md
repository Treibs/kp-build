---
id: ownership-transfer-green
statement: 'To make an object freely transferable from any module via `transfer::public_transfer`,
  declare it with both abilities: `public struct Item has key, store { id: UID }`
  — `public_transfer<T: key + store>` requires `store`.'
paper: ''
supporting_passage: sui 1.74.1 builds `transfer::public_transfer` applied to a struct
  declared `has key, store` with exit 0.
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
  artifact: sui-move-fixtures/ownership-transfer-green
grounding: {}
judgment: {}
---

To make an object freely transferable from any module via `transfer::public_transfer`, declare it with both abilities: `public struct Item has key, store { id: UID }` — `public_transfer<T: key + store>` requires `store`.

> sui 1.74.1 builds `transfer::public_transfer` applied to a struct declared `has key, store` with exit 0.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
