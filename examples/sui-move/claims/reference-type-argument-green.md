---
id: reference-type-argument-green
statement: References are never stored or passed as type arguments — hold the copyable
  `ID` (`Option<ID>`, `object::id(&obj)`) and borrow at the point of use.
paper: ''
supporting_passage: sui 1.74.1 builds a module storing Option<ID> and recording via
  object::id, exit 0, zero warnings.
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
  artifact: sui-move-fixtures/reference-type-argument-green
grounding: {}
judgment: {}
---

References are never stored or passed as type arguments — hold the copyable `ID` (`Option<ID>`, `object::id(&obj)`) and borrow at the point of use.

> sui 1.74.1 builds a module storing Option<ID> and recording via object::id, exit 0, zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
