---
id: uid-to-address-green
statement: UID-to-address is `object::uid_to_address(&x.id)`; whole-object-to-address
  is `object::id_address(&obj)`. Both build green on sui 1.74.1.
paper: ''
supporting_passage: sui 1.74.1 builds a module deriving addresses via object::uid_to_address
  and object::id_address, exit 0, zero warnings.
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
  artifact: sui-move-fixtures/uid-to-address-green
grounding: {}
judgment: {}
---

UID-to-address is `object::uid_to_address(&x.id)`; whole-object-to-address is `object::id_address(&obj)`. Both build green on sui 1.74.1.

> sui 1.74.1 builds a module deriving addresses via object::uid_to_address and object::id_address, exit 0, zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
