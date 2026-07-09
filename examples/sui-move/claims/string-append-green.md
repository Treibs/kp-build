---
id: string-append-green
statement: 'String concatenation in Move is the in-place `append`: `a.append(b)` (or
  `string::append(&mut a, b)`), mutating the left string through `&mut`. To build
  up a string, declare it `mut` and append pieces.'
paper: ''
supporting_passage: sui 1.74.1 builds a module concatenating with `a.append(b)` on
  `std::string::String` values, with exit 0 and zero warnings.
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
  checked: '2026-07-09'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/string-append-green
grounding: {}
judgment: {}
---

String concatenation in Move is the in-place `append`: `a.append(b)` (or `string::append(&mut a, b)`), mutating the left string through `&mut`. To build up a string, declare it `mut` and append pieces.

> sui 1.74.1 builds a module concatenating with `a.append(b)` on `std::string::String` values, with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
