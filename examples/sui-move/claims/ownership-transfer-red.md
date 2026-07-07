---
id: ownership-transfer-red
statement: 'Calling `transfer::public_transfer` on a `key`-only struct (no `store`)
  does not compile: sui 1.74.1 fails with error[E05001] ability constraint not satisfied
  — "The type ''ownership_transfer_red::item::Item'' does not have the ability ''store''".
  For key-only types, use `transfer::transfer` from the defining module instead.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects `transfer::public_transfer` on a struct with
  only `key` with exit 1, error[E05001]: ability constraint not satisfied (missing
  `store`).'
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
  checked: '2026-07-07'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/ownership-transfer-red
grounding: {}
judgment: {}
---

Calling `transfer::public_transfer` on a `key`-only struct (no `store`) does not compile: sui 1.74.1 fails with error[E05001] ability constraint not satisfied — "The type 'ownership_transfer_red::item::Item' does not have the ability 'store'". For key-only types, use `transfer::transfer` from the defining module instead.

> sui 1.74.1 rejects `transfer::public_transfer` on a struct with only `key` with exit 1, error[E05001]: ability constraint not satisfied (missing `store`).

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
