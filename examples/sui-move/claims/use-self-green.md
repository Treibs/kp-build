---
id: use-self-green
statement: 'In `use` group imports, the module itself is named with the capital `Self`
  keyword: `use sui::coin::{Self, Coin};` binds both the module alias `coin` and the
  type `Coin`.'
paper: ''
supporting_passage: sui 1.74.1 (edition 2024) builds a module importing `use sui::coin::{Self,
  Coin};` and calling `coin::value` with exit 0.
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
  artifact: sui-move-fixtures/use-self-green
grounding: {}
judgment: {}
---

In `use` group imports, the module itself is named with the capital `Self` keyword: `use sui::coin::{Self, Coin};` binds both the module alias `coin` and the type `Coin`.

> sui 1.74.1 (edition 2024) builds a module importing `use sui::coin::{Self, Coin};` and calling `coin::value` with exit 0.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
