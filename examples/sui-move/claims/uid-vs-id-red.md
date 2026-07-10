---
id: uid-vs-id-red
statement: '`object::id` takes `&T` where `T: key` — feeding it the raw `&UID` fails
  on sui 1.74.1 with error[E05001]: "The type ''sui::object::UID'' does not have the
  ability ''key''". A `UID` is not the identity value; convert with `uid_to_inner`.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects object::id(&pet.id) with exit 1, error[E05001]:
  ability constraint not satisfied, The type ''sui::object::UID'' does not have the
  ability ''key''.'
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
  artifact: sui-move-fixtures/uid-vs-id-red
grounding: {}
judgment: {}
---

`object::id` takes `&T` where `T: key` — feeding it the raw `&UID` fails on sui 1.74.1 with error[E05001]: "The type 'sui::object::UID' does not have the ability 'key'". A `UID` is not the identity value; convert with `uid_to_inner`.

> sui 1.74.1 rejects object::id(&pet.id) with exit 1, error[E05001]: ability constraint not satisfied, The type 'sui::object::UID' does not have the ability 'key'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
