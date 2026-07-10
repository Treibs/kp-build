---
id: use-self-red
statement: 'Rust-style lowercase `self` in a group import does not exist in Move:
  `use sui::coin::{self, Coin};` fails on sui 1.74.1 with error[E03003] unbound module
  member — "Invalid ''use''. Unbound member ''self'' in module ''sui::coin''" (and
  the module alias is then unresolvable). Use capital `Self`.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects `use sui::coin::{self, Coin};` with exit 1,
  error[E03003]: Invalid ''use''. Unbound member ''self'' in module ''sui::coin''.'
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
  artifact: sui-move-fixtures/use-self-red
grounding: {}
judgment: {}
---

Rust-style lowercase `self` in a group import does not exist in Move: `use sui::coin::{self, Coin};` fails on sui 1.74.1 with error[E03003] unbound module member — "Invalid 'use'. Unbound member 'self' in module 'sui::coin'" (and the module alias is then unresolvable). Use capital `Self`.

> sui 1.74.1 rejects `use sui::coin::{self, Coin};` with exit 1, error[E03003]: Invalid 'use'. Unbound member 'self' in module 'sui::coin'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
