---
id: otw-init-green
statement: 'A module initializer is `fun init(witness: OTW, ctx: &mut TxContext)`
  (or `fun init(ctx: &mut TxContext)`); the one-time witness is a field-less, `drop`-only
  struct named after the module in all uppercase, e.g. `public struct DEMO has drop
  {}` in module `demo`.'
paper: ''
supporting_passage: sui 1.74.1 builds a module whose `init` takes a correctly-shaped
  one-time witness (`public struct DEMO has drop {}` in module `demo`) as its first
  parameter, exit 0.
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
  artifact: sui-move-fixtures/otw-init-green
grounding: {}
judgment: {}
---

A module initializer is `fun init(witness: OTW, ctx: &mut TxContext)` (or `fun init(ctx: &mut TxContext)`); the one-time witness is a field-less, `drop`-only struct named after the module in all uppercase, e.g. `public struct DEMO has drop {}` in module `demo`.

> sui 1.74.1 builds a module whose `init` takes a correctly-shaped one-time witness (`public struct DEMO has drop {}` in module `demo`) as its first parameter, exit 0.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
