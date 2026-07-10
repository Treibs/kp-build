---
id: vector-destroy-empty-red
statement: 'Draining a `vector<T>` (T without `drop`) to empty is not enough — dropping
  the emptied vector fails on sui 1.74.1 with error[E06001]: "The parameter ''rockets''
  still contains a value" (the ability system does not know the vector is empty).
  Call `vector::destroy_empty`.'
paper: ''
supporting_passage: sui 1.74.1 rejects a fully-drained vector<Rocket> left to drop
  at the closing brace, exit 1, error[E06001], The parameter 'rockets' still contains
  a value.
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
  artifact: sui-move-fixtures/vector-destroy-empty-red
grounding: {}
judgment: {}
---

Draining a `vector<T>` (T without `drop`) to empty is not enough — dropping the emptied vector fails on sui 1.74.1 with error[E06001]: "The parameter 'rockets' still contains a value" (the ability system does not know the vector is empty). Call `vector::destroy_empty`.

> sui 1.74.1 rejects a fully-drained vector<Rocket> left to drop at the closing brace, exit 1, error[E06001], The parameter 'rockets' still contains a value.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
