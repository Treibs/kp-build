---
id: balance-api-on-coin-green
statement: An accumulating pool field is a `Balance<T>`; `Coin` is the boundary type
  — `coin::put(&mut pool, payment)` deposits a `Coin`, `coin::take(&mut pool, amount,
  ctx)` mints a `Coin` back out.
paper: ''
supporting_passage: sui 1.74.1 builds a till module with a Balance<SUI> field, coin::put
  pay-in and coin::take pay-out, exit 0, zero warnings.
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
  artifact: sui-move-fixtures/balance-api-on-coin-green
grounding: {}
judgment: {}
---

An accumulating pool field is a `Balance<T>`; `Coin` is the boundary type — `coin::put(&mut pool, payment)` deposits a `Coin`, `coin::take(&mut pool, amount, ctx)` mints a `Coin` back out.

> sui 1.74.1 builds a till module with a Balance<SUI> field, coin::put pay-in and coin::take pay-out, exit 0, zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
