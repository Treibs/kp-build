---
id: destructure-ignore-green
statement: 'Dismantling an object binds its non-`drop` fields and consumes them explicitly:
  `let Crate { id } = c; object::delete(id);` builds green — the `UID` is destroyed
  by `object::delete`, not ignored.'
paper: ''
supporting_passage: sui 1.74.1 builds a module that destructures a `key` object with
  `let Crate { id } = c` and consumes the `UID` via `object::delete(id)`, with exit
  0 and zero warnings.
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
  artifact: sui-move-fixtures/destructure-ignore-green
grounding: {}
judgment: {}
---

Dismantling an object binds its non-`drop` fields and consumes them explicitly: `let Crate { id } = c; object::delete(id);` builds green — the `UID` is destroyed by `object::delete`, not ignored.

> sui 1.74.1 builds a module that destructures a `key` object with `let Crate { id } = c` and consumes the `UID` via `object::delete(id)`, with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
