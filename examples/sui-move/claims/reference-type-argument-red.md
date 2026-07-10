---
id: reference-type-argument-red
statement: 'A reference cannot be a type argument: `stamp: Option<&Stamp>` fails on
  sui 1.74.1 with error[E04004] — "Expected a single non-reference type". References
  are not first-class values in Move.'
paper: ''
supporting_passage: sui 1.74.1 rejects Option<&Stamp> as a parameter type with exit
  1, error[E04004], Expected a single non-reference type.
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
  artifact: sui-move-fixtures/reference-type-argument-red
grounding: {}
judgment: {}
---

A reference cannot be a type argument: `stamp: Option<&Stamp>` fails on sui 1.74.1 with error[E04004] — "Expected a single non-reference type". References are not first-class values in Move.

> sui 1.74.1 rejects Option<&Stamp> as a parameter type with exit 1, error[E04004], Expected a single non-reference type.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
