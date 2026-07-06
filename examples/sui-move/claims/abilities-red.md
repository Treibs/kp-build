---
id: abilities-red
statement: 'A `key` struct whose first field is not `id: UID` (e.g. `public struct
  Item has key { value: u64 }`) does not compile: sui 1.74.1 fails with error[Sui
  E02007] invalid object declaration — "Structs with the ''key'' ability must have
  ''id: sui::object::UID'' as their first field".'
paper: ''
supporting_passage: 'sui 1.74.1 rejects a `key` struct missing the leading `id: UID`
  field with exit 1, error[Sui E02007]: invalid object declaration.'
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
  checked: '2026-07-06'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/abilities-red
grounding: {}
judgment: {}
---

A `key` struct whose first field is not `id: UID` (e.g. `public struct Item has key { value: u64 }`) does not compile: sui 1.74.1 fails with error[Sui E02007] invalid object declaration — "Structs with the 'key' ability must have 'id: sui::object::UID' as their first field".

> sui 1.74.1 rejects a `key` struct missing the leading `id: UID` field with exit 1, error[Sui E02007]: invalid object declaration.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
