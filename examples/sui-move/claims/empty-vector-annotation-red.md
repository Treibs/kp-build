---
id: empty-vector-annotation-red
statement: '`let owners = vector::empty();` with no annotation and no later element
  evidence fails inference on sui 1.74.1: error[E04010] — "Could not infer this type.
  Try adding an annotation". Same class as the struct-literal `vector[]` shape recorded
  in round 4.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects an unannotated vector::empty() whose only
  use is vector::length, exit 1, error[E04010]: cannot infer type, Could not infer
  this type. Try adding an annotation.'
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
  artifact: sui-move-fixtures/empty-vector-annotation-red
grounding: {}
judgment: {}
---

`let owners = vector::empty();` with no annotation and no later element evidence fails inference on sui 1.74.1: error[E04010] — "Could not infer this type. Try adding an annotation". Same class as the struct-literal `vector[]` shape recorded in round 4.

> sui 1.74.1 rejects an unannotated vector::empty() whose only use is vector::length, exit 1, error[E04010]: cannot infer type, Could not infer this type. Try adding an annotation.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
