---
id: missing-module-import-green
statement: 'Calling a module''s function through its alias (`event::emit(...)`) requires
  the alias to be bound first with a `use` declaration: `use sui::event;` then `event::emit(Ping
  { value })` builds green.'
paper: ''
supporting_passage: sui 1.74.1 builds a module with `use sui::event;` and an `event::emit(Ping
  { value })` call, with exit 0 and zero warnings.
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
  artifact: sui-move-fixtures/missing-module-import-green
grounding: {}
judgment: {}
---

Calling a module's function through its alias (`event::emit(...)`) requires the alias to be bound first with a `use` declaration: `use sui::event;` then `event::emit(Ping { value })` builds green.

> sui 1.74.1 builds a module with `use sui::event;` and an `event::emit(Ping { value })` call, with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
