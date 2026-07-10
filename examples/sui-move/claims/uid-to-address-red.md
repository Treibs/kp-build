---
id: uid-to-address-red
statement: '`object::id_to_address` takes an `&ID`, not a `&UID`: `object::id_to_address(&inv.id)`
  fails on sui 1.74.1 with error[E04007] incompatible types — "Invalid call of ''sui::object::id_to_address''.
  Invalid argument for parameter ''id''".'
paper: ''
supporting_passage: 'sui 1.74.1 rejects object::id_to_address(&inv.id) on a UID field
  with exit 1, error[E04007]: incompatible types, Invalid call of ''sui::object::id_to_address''.
  Invalid argument for parameter ''id''.'
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
  artifact: sui-move-fixtures/uid-to-address-red
grounding: {}
judgment: {}
---

`object::id_to_address` takes an `&ID`, not a `&UID`: `object::id_to_address(&inv.id)` fails on sui 1.74.1 with error[E04007] incompatible types — "Invalid call of 'sui::object::id_to_address'. Invalid argument for parameter 'id'".

> sui 1.74.1 rejects object::id_to_address(&inv.id) on a UID field with exit 1, error[E04007]: incompatible types, Invalid call of 'sui::object::id_to_address'. Invalid argument for parameter 'id'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
