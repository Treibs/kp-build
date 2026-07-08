---
id: param-mut-green
statement: 'Assigning through a by-value function parameter requires `mut` on the
  parameter, the same keyword `let mut` requires for locals: `public fun bump(mut
  c: Counter)` with `c.n = c.n + 1` builds green.'
paper: ''
supporting_passage: 'sui 1.74.1 builds a module whose function takes `mut c: Counter`
  by value and assigns `c.n = c.n + 1`, with exit 0 and zero warnings.'
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
  checked: '2026-07-08'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/param-mut-green
grounding: {}
judgment: {}
---

Assigning through a by-value function parameter requires `mut` on the parameter, the same keyword `let mut` requires for locals: `public fun bump(mut c: Counter)` with `c.n = c.n + 1` builds green.

> sui 1.74.1 builds a module whose function takes `mut c: Counter` by value and assigns `c.n = c.n + 1`, with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
