---
id: value-consumption-paths-green
statement: 'A non-`drop` parameter (e.g. `payment: Coin<SUI>`) must be consumed on
  EVERY path — including the no-op/losing branch. The composable pattern returns it
  to the caller (e.g. `Option<Coin<SUI>>`: `none` after consuming, `some(payment)`
  on the path that doesn''t).'
paper: ''
supporting_passage: sui 1.74.1 builds a module whose losing branch hands the Coin
  back via option::some, exit 0, zero warnings.
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
  artifact: sui-move-fixtures/value-consumption-paths-green
grounding: {}
judgment: {}
---

A non-`drop` parameter (e.g. `payment: Coin<SUI>`) must be consumed on EVERY path — including the no-op/losing branch. The composable pattern returns it to the caller (e.g. `Option<Coin<SUI>>`: `none` after consuming, `some(payment)` on the path that doesn't).

> sui 1.74.1 builds a module whose losing branch hands the Coin back via option::some, exit 0, zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
