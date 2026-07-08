---
id: dynamic-fields-green
statement: 'Dynamic fields live in the `sui::dynamic_field` module: `use sui::dynamic_field;`
  then `dynamic_field::add(&mut obj.id, name, value)` to attach and `dynamic_field::borrow(&obj.id,
  name)` to read.'
paper: ''
supporting_passage: sui 1.74.1 builds `dynamic_field::add` / `dynamic_field::borrow`
  operating on `&mut container.id` / `&container.id` with exit 0.
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
  artifact: sui-move-fixtures/dynamic-fields-green
grounding: {}
judgment: {}
---

Dynamic fields live in the `sui::dynamic_field` module: `use sui::dynamic_field;` then `dynamic_field::add(&mut obj.id, name, value)` to attach and `dynamic_field::borrow(&obj.id, name)` to read.

> sui 1.74.1 builds `dynamic_field::add` / `dynamic_field::borrow` operating on `&mut container.id` / `&container.id` with exit 0.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
