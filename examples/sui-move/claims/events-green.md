---
id: events-green
statement: 'Event structs must have both `copy` and `drop`: `public struct ValueSet
  has copy, drop { value: u64 }` emitted with `sui::event::emit(ValueSet { value })`.'
paper: ''
supporting_passage: sui 1.74.1 builds `event::emit` on a struct declared `has copy,
  drop` with exit 0.
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
  artifact: sui-move-fixtures/events-green
grounding: {}
judgment: {}
---

Event structs must have both `copy` and `drop`: `public struct ValueSet has copy, drop { value: u64 }` emitted with `sui::event::emit(ValueSet { value })`.

> sui 1.74.1 builds `event::emit` on a struct declared `has copy, drop` with exit 0.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
