---
id: public-transfer-foreign-red
statement: '`transfer::transfer` on a type defined elsewhere does not compile: it
  is the PRIVATE transfer, restricted to the type''s defining module. sui 1.74.1 rejects
  `transfer::transfer(coin, recipient)` on `Coin<SUI>` in a foreign module with error[Sui
  E02009] invalid private transfer call — "The function ''sui::transfer::transfer''
  is restricted to being called in the object''s module, ''sui::coin''" — and notes
  that `public_transfer` can be called instead because `Coin` has `store`.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects transfer::transfer(coin, recipient) on Coin<SUI>
  outside sui::coin with exit 1, error[Sui E02009]: The function ''sui::transfer::transfer''
  is restricted to being called in the object''s module, ''sui::coin''.'
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
  artifact: sui-move-fixtures/public-transfer-foreign-red
grounding: {}
judgment: {}
---

`transfer::transfer` on a type defined elsewhere does not compile: it is the PRIVATE transfer, restricted to the type's defining module. sui 1.74.1 rejects `transfer::transfer(coin, recipient)` on `Coin<SUI>` in a foreign module with error[Sui E02009] invalid private transfer call — "The function 'sui::transfer::transfer' is restricted to being called in the object's module, 'sui::coin'" — and notes that `public_transfer` can be called instead because `Coin` has `store`.

> sui 1.74.1 rejects transfer::transfer(coin, recipient) on Coin<SUI> outside sui::coin with exit 1, error[Sui E02009]: The function 'sui::transfer::transfer' is restricted to being called in the object's module, 'sui::coin'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
