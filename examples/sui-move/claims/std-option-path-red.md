---
id: std-option-path-red
statement: 'There is no `sui::option`: `use sui::option::{Self, Option};` fails on
  sui 1.74.1 with error[E03002] — "Unbound module: ''sui::option''". The mirror image
  of the SUI-import class: a crowded `sui::` import block pulls the std module under
  the wrong prefix.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects use sui::option with exit 1, error[E03002],
  Unbound module: ''sui::option''.'
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
  checked: '2026-07-10'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/std-option-path-red
grounding: {}
judgment: {}
---

There is no `sui::option`: `use sui::option::{Self, Option};` fails on sui 1.74.1 with error[E03002] — "Unbound module: 'sui::option'". The mirror image of the SUI-import class: a crowded `sui::` import block pulls the std module under the wrong prefix.

> sui 1.74.1 rejects use sui::option with exit 1, error[E03002], Unbound module: 'sui::option'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
