---
id: uid-vs-id-green
statement: 'The copyable identity of an object comes from `object::id(&obj)` (requires
  `T: key`) or `object::uid_to_inner(&obj.id)` from its `UID` — both build green.'
paper: ''
supporting_passage: sui 1.74.1 builds a module deriving ID via object::id(pet) and
  object::uid_to_inner(&pet.id), exit 0, zero warnings.
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
  artifact: sui-move-fixtures/uid-vs-id-green
grounding: {}
judgment: {}
---

The copyable identity of an object comes from `object::id(&obj)` (requires `T: key`) or `object::uid_to_inner(&obj.id)` from its `UID` — both build green.

> sui 1.74.1 builds a module deriving ID via object::id(pet) and object::uid_to_inner(&pet.id), exit 0, zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
