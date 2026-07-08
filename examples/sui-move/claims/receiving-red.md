---
id: receiving-red
statement: 'The internal `transfer::receive` cannot unwrap a `Receiving<T>` when `T`
  is defined in a different module: sui 1.74.1 fails with error[Sui E02009] invalid
  private transfer call — "The function ''sui::transfer::receive'' is restricted to
  being called in the object''s module". Outside the defining module, use `public_receive`
  (which requires `store`).'
paper: ''
supporting_passage: 'sui 1.74.1 rejects a cross-module transfer::receive with exit
  1, error[Sui E02009]: invalid private transfer call — the function is restricted
  to being called in the object''s module.'
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
  artifact: sui-move-fixtures/receiving-red
grounding: {}
judgment: {}
---

The internal `transfer::receive` cannot unwrap a `Receiving<T>` when `T` is defined in a different module: sui 1.74.1 fails with error[Sui E02009] invalid private transfer call — "The function 'sui::transfer::receive' is restricted to being called in the object's module". Outside the defining module, use `public_receive` (which requires `store`).

> sui 1.74.1 rejects a cross-module transfer::receive with exit 1, error[Sui E02009]: invalid private transfer call — the function is restricted to being called in the object's module.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
