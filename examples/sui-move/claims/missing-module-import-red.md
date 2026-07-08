---
id: missing-module-import-red
statement: 'Calling `event::emit(...)` with no `use sui::event` in the module (the
  Rust habit of resolving `mod::fn` paths without a per-module import) fails: sui
  1.74.1 reports error[E03006] unexpected name in this position — "Could not resolve
  the name ''event''". Every `module::fn` alias call needs its module bound by `use`.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects `event::emit(Ping { value })` in a module
  with no `use sui::event`, with exit 1, error[E03006]: unexpected name in this position,
  Could not resolve the name ''event''.'
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
  checked: '2026-07-08'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/missing-module-import-red
grounding: {}
judgment: {}
---

Calling `event::emit(...)` with no `use sui::event` in the module (the Rust habit of resolving `mod::fn` paths without a per-module import) fails: sui 1.74.1 reports error[E03006] unexpected name in this position — "Could not resolve the name 'event'". Every `module::fn` alias call needs its module bound by `use`.

> sui 1.74.1 rejects `event::emit(Ping { value })` in a module with no `use sui::event`, with exit 1, error[E03006]: unexpected name in this position, Could not resolve the name 'event'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
