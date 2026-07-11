---
id: moved-value-arg-order-green
statement: 'Read every field you need into locals BEFORE the value moves: `let destination
  = parcel.addressee;` then `transfer::transfer(parcel, destination)` — arguments
  evaluate left to right and the move happens first.'
paper: ''
supporting_passage: sui 1.74.1 builds a dispatch function hoisting the addressee read
  before the transfer move, exit 0, zero warnings.
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
  checked: '2026-07-10'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/moved-value-arg-order-green
grounding: {}
judgment: {}
---

Read every field you need into locals BEFORE the value moves: `let destination = parcel.addressee;` then `transfer::transfer(parcel, destination)` — arguments evaluate left to right and the move happens first.

> sui 1.74.1 builds a dispatch function hoisting the addressee read before the transfer move, exit 0, zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
