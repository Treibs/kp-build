---
id: tuple-bleed-red
statement: 'A tuple cannot be a type argument: `Option<(u64, address)>` fails on sui
  1.74.1 with error[E04004] — "Expected a single non-reference type, but found: ''(u64,
  address)''". Tuples are expression/return conveniences, not runtime values; the
  same class rejects tuples in storage positions (`vector<(A, B)>`, struct fields).
  Adjacency disclosed: `reference-type-argument-red` pins the reference form under
  the same E04004 family; this zone pins the tuple form with a distinct fragment.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects Option<(u64, address)> as a return type argument
  with exit 1, error[E04004], Expected a single non-reference type, but found: ''(u64,
  address)''.'
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
  artifact: sui-move-fixtures/tuple-bleed-red
grounding: {}
judgment: {}
---

A tuple cannot be a type argument: `Option<(u64, address)>` fails on sui 1.74.1 with error[E04004] — "Expected a single non-reference type, but found: '(u64, address)'". Tuples are expression/return conveniences, not runtime values; the same class rejects tuples in storage positions (`vector<(A, B)>`, struct fields). Adjacency disclosed: `reference-type-argument-red` pins the reference form under the same E04004 family; this zone pins the tuple form with a distinct fragment.

> sui 1.74.1 rejects Option<(u64, address)> as a return type argument with exit 1, error[E04004], Expected a single non-reference type, but found: '(u64, address)'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
