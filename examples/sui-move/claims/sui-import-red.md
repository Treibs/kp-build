---
id: sui-import-red
statement: '`SUI` is not a member of `sui::coin`: `use sui::coin::{Self, Coin, SUI}`
  fails on sui 1.74.1 with error[E03003] unbound module member — "Unbound member ''SUI''
  in module ''sui::coin''". This wrong-module shape is the pack''s most-recorded held-out
  class (×6 across experiments); the absent-import shape fails the same way at the
  first use site.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects `use sui::coin::{Self, Coin, SUI}` with exit
  1, error[E03003]: unbound module member, Unbound member ''SUI'' in module ''sui::coin''.'
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
  artifact: sui-move-fixtures/sui-import-red
grounding: {}
judgment: {}
---

`SUI` is not a member of `sui::coin`: `use sui::coin::{Self, Coin, SUI}` fails on sui 1.74.1 with error[E03003] unbound module member — "Unbound member 'SUI' in module 'sui::coin'". This wrong-module shape is the pack's most-recorded held-out class (×6 across experiments); the absent-import shape fails the same way at the first use site.

> sui 1.74.1 rejects `use sui::coin::{Self, Coin, SUI}` with exit 1, error[E03003]: unbound module member, Unbound member 'SUI' in module 'sui::coin'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
