---
id: public-transfer-foreign-green
statement: To transfer an object whose type is defined in ANOTHER module — e.g. `Coin<SUI>`,
  which has `store` — call `transfer::public_transfer(obj, recipient)`. The public
  variant is the one callable outside the type's defining module; this is the mirror
  of the rule that `transfer::transfer` works only in-module.
paper: ''
supporting_passage: sui 1.74.1 builds a foreign module calling `transfer::public_transfer(coin,
  recipient)` on `Coin<SUI>` with exit 0 and zero warnings.
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
  artifact: sui-move-fixtures/public-transfer-foreign-green
grounding: {}
judgment: {}
---

To transfer an object whose type is defined in ANOTHER module — e.g. `Coin<SUI>`, which has `store` — call `transfer::public_transfer(obj, recipient)`. The public variant is the one callable outside the type's defining module; this is the mirror of the rule that `transfer::transfer` works only in-module.

> sui 1.74.1 builds a foreign module calling `transfer::public_transfer(coin, recipient)` on `Coin<SUI>` with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
