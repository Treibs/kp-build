---
id: coin-currency-red
statement: 'There is no `coin::mint_new`: the fabricated `coin::mint_new(witness,
  9, b"MYC", ctx)` fails on sui 1.74.1 with error[E03003] unbound module member —
  "Unbound function ''mint_new'' in module ''sui::coin''".'
paper: ''
supporting_passage: 'sui 1.74.1 rejects a call to the nonexistent `coin::mint_new`
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
  artifact: sui-move-fixtures/coin-currency-red
grounding: {}
judgment: {}
---

There is no `coin::mint_new`: the fabricated `coin::mint_new(witness, 9, b"MYC", ctx)` fails on sui 1.74.1 with error[E03003] unbound module member — "Unbound function 'mint_new' in module 'sui::coin'".

> sui 1.74.1 rejects a call to the nonexistent `coin::mint_new` with exit 1, error[E03003]: unbound module member.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
