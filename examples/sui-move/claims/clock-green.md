---
id: clock-green
statement: 'On-chain time comes from `sui::clock::Clock` (a shared object at address
  0x6): take `clock: &Clock` as a function parameter and read milliseconds with `clock.timestamp_ms()`.'
paper: ''
supporting_passage: 'sui 1.74.1 builds a function taking `clock: &Clock` and calling
  `clock.timestamp_ms()` with exit 0.'
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
  checked: '2026-07-06'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/clock-green
grounding: {}
judgment: {}
---

On-chain time comes from `sui::clock::Clock` (a shared object at address 0x6): take `clock: &Clock` as a function parameter and read milliseconds with `clock.timestamp_ms()`.

> sui 1.74.1 builds a function taking `clock: &Clock` and calling `clock.timestamp_ms()` with exit 0.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
