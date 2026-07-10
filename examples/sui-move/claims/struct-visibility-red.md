---
id: struct-visibility-red
statement: 'The pre-2024 form `struct Counter has key { ... }` (bare `struct`, no
  visibility modifier) does not compile in edition 2024: sui 1.74.1 fails with error[E01003]
  invalid modifier — "Visibility annotations are required on struct declarations".'
paper: ''
supporting_passage: 'sui 1.74.1 rejects a bare `struct Counter has key` declaration
  with exit 1, error[E01003]: invalid modifier, noting that visibility annotations
  are required on struct declarations.'
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
  artifact: sui-move-fixtures/struct-visibility-red
grounding: {}
judgment: {}
---

The pre-2024 form `struct Counter has key { ... }` (bare `struct`, no visibility modifier) does not compile in edition 2024: sui 1.74.1 fails with error[E01003] invalid modifier — "Visibility annotations are required on struct declarations".

> sui 1.74.1 rejects a bare `struct Counter has key` declaration with exit 1, error[E01003]: invalid modifier, noting that visibility annotations are required on struct declarations.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
