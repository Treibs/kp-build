---
id: param-mut-red
statement: 'Mutating a by-value parameter not declared `mut` fails: `fun bump(c: Counter)`
  with `c.n = c.n + 1` is rejected by sui 1.74.1 with error[E04024] invalid usage
  of immutable variable — "To use the variable mutably, it must be declared ''mut''".
  Move 2024''s `mut` requirement covers function parameters, not just `let` bindings.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects an assignment through a non-`mut` by-value
  parameter, with exit 1, error[E04024]: invalid usage of immutable variable, To use
  the variable mutably, it must be declared ''mut''.'
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
  checked: '2026-07-09'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/param-mut-red
grounding: {}
judgment: {}
---

Mutating a by-value parameter not declared `mut` fails: `fun bump(c: Counter)` with `c.n = c.n + 1` is rejected by sui 1.74.1 with error[E04024] invalid usage of immutable variable — "To use the variable mutably, it must be declared 'mut'". Move 2024's `mut` requirement covers function parameters, not just `let` bindings.

> sui 1.74.1 rejects an assignment through a non-`mut` by-value parameter, with exit 1, error[E04024]: invalid usage of immutable variable, To use the variable mutably, it must be declared 'mut'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
