---
id: struct-visibility-green
statement: 'In Move 2024, declare structs with an explicit visibility modifier: `public
  struct Counter has key { id: UID, value: u64 }`. `public` is currently the only
  struct visibility modifier.'
paper: ''
supporting_passage: 'sui 1.74.1 (edition 2024) builds a module whose struct is declared
  `public struct Counter has key { id: UID, value: u64 }` with exit 0.'
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
  artifact: sui-move-fixtures/struct-visibility-green
grounding: {}
judgment: {}
---

In Move 2024, declare structs with an explicit visibility modifier: `public struct Counter has key { id: UID, value: u64 }`. `public` is currently the only struct visibility modifier.

> sui 1.74.1 (edition 2024) builds a module whose struct is declared `public struct Counter has key { id: UID, value: u64 }` with exit 0.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
