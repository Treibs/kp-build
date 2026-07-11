---
id: balance-api-on-coin-red
statement: '`coin::put`/`coin::take` operate on `&mut Balance<T>`, not on `Coin`:
  storing the pool as `Coin<SUI>` and calling `coin::put(&mut till.funds, payment)`
  fails on sui 1.74.1 with error[E04007] — "Invalid call of ''sui::coin::put''. Invalid
  argument for parameter ''balance''".'
paper: ''
supporting_passage: sui 1.74.1 rejects coin::put on a Coin<SUI> field with exit 1,
  error[E04007], Invalid call of 'sui::coin::put'. Invalid argument for parameter
  'balance'.
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
  artifact: sui-move-fixtures/balance-api-on-coin-red
grounding: {}
judgment: {}
---

`coin::put`/`coin::take` operate on `&mut Balance<T>`, not on `Coin`: storing the pool as `Coin<SUI>` and calling `coin::put(&mut till.funds, payment)` fails on sui 1.74.1 with error[E04007] — "Invalid call of 'sui::coin::put'. Invalid argument for parameter 'balance'".

> sui 1.74.1 rejects coin::put on a Coin<SUI> field with exit 1, error[E04007], Invalid call of 'sui::coin::put'. Invalid argument for parameter 'balance'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
