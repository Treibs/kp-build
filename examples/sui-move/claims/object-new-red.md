---
id: object-new-red
statement: 'The probed `object::uid_from_bytes` does not exist (Unbound function ''uid_from_bytes''
  in module ''sui::object''): sui 1.74.1 fails with error[E03003] unbound module member.
  `UID`s are created with `object::new(ctx)`.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects a call to the nonexistent `object::uid_from_bytes`
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
  checked: '2026-07-09'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/object-new-red
grounding: {}
judgment: {}
---

The probed `object::uid_from_bytes` does not exist (Unbound function 'uid_from_bytes' in module 'sui::object'): sui 1.74.1 fails with error[E03003] unbound module member. `UID`s are created with `object::new(ctx)`.

> sui 1.74.1 rejects a call to the nonexistent `object::uid_from_bytes` with exit 1, error[E03003]: unbound module member.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
