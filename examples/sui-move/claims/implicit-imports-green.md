---
id: implicit-imports-green
statement: 'In edition 2024 with the Sui framework, `UID`, `object`, `transfer`, and
  `TxContext` are available with no `use` declarations: write `public struct Counter
  has key { id: UID, ... }`, `object::new(ctx)`, and `transfer::share_object(...)`
  without any import block.'
paper: ''
supporting_passage: sui 1.74.1 builds a module that uses UID, object::new, transfer::share_object,
  and TxContext with zero `use` statements, exit 0.
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
  artifact: sui-move-fixtures/implicit-imports-green
grounding: {}
judgment: {}
---

In edition 2024 with the Sui framework, `UID`, `object`, `transfer`, and `TxContext` are available with no `use` declarations: write `public struct Counter has key { id: UID, ... }`, `object::new(ctx)`, and `transfer::share_object(...)` without any import block.

> sui 1.74.1 builds a module that uses UID, object::new, transfer::share_object, and TxContext with zero `use` statements, exit 0.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
