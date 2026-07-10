---
id: std-mem-swap-red
statement: 'There is no `std::mem` module in Move: `std::mem::swap(&mut d.slot, &mut
  old)` is rejected by sui 1.74.1 with error[E03002] unbound module — "Unbound module
  ''std::mem''". Rust''s `mem::swap`/`mem::replace` idiom does not exist; use an `Option`
  slot with `std::option::swap`.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects `std::mem::swap(&mut d.slot, &mut old)` with
  exit 1, error[E03002]: unbound module, Unbound module ''std::mem''.'
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
  artifact: sui-move-fixtures/std-mem-swap-red
grounding: {}
judgment: {}
---

There is no `std::mem` module in Move: `std::mem::swap(&mut d.slot, &mut old)` is rejected by sui 1.74.1 with error[E03002] unbound module — "Unbound module 'std::mem'". Rust's `mem::swap`/`mem::replace` idiom does not exist; use an `Option` slot with `std::option::swap`.

> sui 1.74.1 rejects `std::mem::swap(&mut d.slot, &mut old)` with exit 1, error[E03002]: unbound module, Unbound module 'std::mem'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
