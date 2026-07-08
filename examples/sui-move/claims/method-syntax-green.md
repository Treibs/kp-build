---
id: method-syntax-green
statement: 'In Move 2024, call functions on their first argument with dot notation:
  a function `public fun value(self: &Counter): u64` defined in the type''s module
  is automatically usable as `counter.value()`. For package-internal access use `public(package)
  fun`, not friend declarations.'
paper: ''
supporting_passage: 'sui 1.74.1 builds a module that defines `public fun value(self:
  &Counter): u64` and calls it via method syntax `counter.value()` with exit 0.'
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
  artifact: sui-move-fixtures/method-syntax-green
grounding: {}
judgment: {}
---

In Move 2024, call functions on their first argument with dot notation: a function `public fun value(self: &Counter): u64` defined in the type's module is automatically usable as `counter.value()`. For package-internal access use `public(package) fun`, not friend declarations.

> sui 1.74.1 builds a module that defines `public fun value(self: &Counter): u64` and calls it via method syntax `counter.value()` with exit 0.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
