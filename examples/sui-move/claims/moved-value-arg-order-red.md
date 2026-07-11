---
id: moved-value-arg-order-red
statement: 'A value moved as an earlier argument cannot be read in a later argument:
  `transfer::transfer(parcel, parcel.addressee)` fails on sui 1.74.1 with error[E06002]
  — "Invalid usage of previously moved variable ''parcel''." The read must be hoisted
  into a local before the move.'
paper: ''
supporting_passage: sui 1.74.1 rejects transfer::transfer(parcel, parcel.addressee)
  with exit 1, error[E06002], Invalid usage of previously moved variable 'parcel'.
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
  artifact: sui-move-fixtures/moved-value-arg-order-red
grounding: {}
judgment: {}
---

A value moved as an earlier argument cannot be read in a later argument: `transfer::transfer(parcel, parcel.addressee)` fails on sui 1.74.1 with error[E06002] — "Invalid usage of previously moved variable 'parcel'." The read must be hoisted into a local before the move.

> sui 1.74.1 rejects transfer::transfer(parcel, parcel.addressee) with exit 1, error[E06002], Invalid usage of previously moved variable 'parcel'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
