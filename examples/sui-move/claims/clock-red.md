---
id: clock-red
statement: '`tx_context::now_ms` does not exist (Unbound function ''now_ms'' in module
  ''sui::tx_context''): sui 1.74.1 fails with error[E03003] unbound module member.
  On-chain time comes from the `Clock` object.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects a call to the nonexistent `tx_context::now_ms`
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
  checked: '2026-07-08'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/clock-red
grounding: {}
judgment: {}
---

`tx_context::now_ms` does not exist (Unbound function 'now_ms' in module 'sui::tx_context'): sui 1.74.1 fails with error[E03003] unbound module member. On-chain time comes from the `Clock` object.

> sui 1.74.1 rejects a call to the nonexistent `tx_context::now_ms` with exit 1, error[E03003]: unbound module member.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
