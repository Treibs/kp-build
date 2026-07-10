---
id: option-field-fill-green
statement: 'To set an `Option<T>` field that is currently `none`, use `option::fill`
  (method syntax `opt.fill(value)`): it adds the value in place and aborts if the
  option is already occupied — no old value is discarded, so `T` needs no `drop` ability.'
paper: ''
supporting_passage: sui 1.74.1 builds a module calling `slot.item.fill(item)` on an
  `Option<Item>` field where `Item` has `store` but no `drop`, with exit 0 and zero
  warnings.
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
  checked: '2026-07-10'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/option-field-fill-green
grounding: {}
judgment: {}
---

To set an `Option<T>` field that is currently `none`, use `option::fill` (method syntax `opt.fill(value)`): it adds the value in place and aborts if the option is already occupied — no old value is discarded, so `T` needs no `drop` ability.

> sui 1.74.1 builds a module calling `slot.item.fill(item)` on an `Option<Item>` field where `Item` has `store` but no `drop`, with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
