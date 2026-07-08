---
id: otw-init-red
statement: 'The `init` signature is checked at build time: an `init` whose first parameter
  is not a one-time witness (e.g. `fun init(value: u64, ctx: &mut TxContext)`) fails
  on sui 1.74.1 with error[Sui E02003] invalid ''init'' function — "Invalid parameter
  ''value'' of type ''u64''. Expected a one-time witness type".'
paper: ''
supporting_passage: 'sui 1.74.1 rejects an `init` function whose first parameter is
  a plain `u64` with exit 1, error[Sui E02003]: invalid ''init'' function — init signatures
  are enforced at build time, not only at publish.'
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
  artifact: sui-move-fixtures/otw-init-red
grounding: {}
judgment: {}
---

The `init` signature is checked at build time: an `init` whose first parameter is not a one-time witness (e.g. `fun init(value: u64, ctx: &mut TxContext)`) fails on sui 1.74.1 with error[Sui E02003] invalid 'init' function — "Invalid parameter 'value' of type 'u64'. Expected a one-time witness type".

> sui 1.74.1 rejects an `init` function whose first parameter is a plain `u64` with exit 1, error[Sui E02003]: invalid 'init' function — init signatures are enforced at build time, not only at publish.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
