---
id: dynamic-fields-red
statement: 'The commonly hallucinated `object::add_field` does not exist (Unbound
  function ''add_field'' in module ''sui::object''): sui 1.74.1 fails with error[E03003]
  unbound module member. Dynamic fields live in `sui::dynamic_field`.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects a call to the nonexistent `object::add_field`
  with exit 1, error[E03003]: unbound module member.'
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
  checked: '2026-07-07'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/dynamic-fields-red
grounding: {}
judgment: {}
---

The commonly hallucinated `object::add_field` does not exist (Unbound function 'add_field' in module 'sui::object'): sui 1.74.1 fails with error[E03003] unbound module member. Dynamic fields live in `sui::dynamic_field`.

> sui 1.74.1 rejects a call to the nonexistent `object::add_field` with exit 1, error[E03003]: unbound module member.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
