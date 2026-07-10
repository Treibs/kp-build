---
id: receiving-doc
statement: 'An object sent to another object arrives in a transaction as `sui::transfer::Receiving<T>`,
  not as `T`: the wrapper indicates the object is owned by another object rather than
  the sender, and `sui::transfer::receive` is called with the parent object to unwrap
  it and prove ownership.'
paper: ''
supporting_passage: Object inputs have the type `T` of the underlying object. `ObjectArg::Receiving`
  inputs are the exception and have type `sui::transfer::Receiving<T>`. This wrapper
  indicates the object is owned by another object, not the sender. Call `sui::transfer::receive`
  with the parent object to unwrap it and prove ownership.
claim_type: method
confidence: high
corroborated_by: []
survived_refuter: true
grounded: unchecked
verified:
  exists: true
  status: verified
  kind: grounding
  via: doc-corpus
  canonical_title: ''
  match_score: 0.0
  evidence: Object inputs have the type `T` of the underlying object. `ObjectArg::Receiving`
    inputs are the exception and have type `sui::transfer::Receiving<T>`. This wrap
  checked: '2026-07-10'
execution: {}
grounding:
  source: sui-docs-concepts
  supporting_passage: Object inputs have the type `T` of the underlying object. `ObjectArg::Receiving`
    inputs are the exception and have type `sui::transfer::Receiving<T>`. This wrapper
    indicates the object is owned by another object, not the sender. Call `sui::transfer::receive`
    with the parent object to unwrap it and prove ownership.
judgment: {}
---

An object sent to another object arrives in a transaction as `sui::transfer::Receiving<T>`, not as `T`: the wrapper indicates the object is owned by another object rather than the sender, and `sui::transfer::receive` is called with the parent object to unwrap it and prove ownership.

> Object inputs have the type `T` of the underlying object. `ObjectArg::Receiving` inputs are the exception and have type `sui::transfer::Receiving<T>`. This wrapper indicates the object is owned by another object, not the sender. Call `sui::transfer::receive` with the parent object to unwrap it and prove ownership.

— *grounding verified* via doc-corpus: Object inputs have the type `T` of the underlying object. `ObjectArg::Receiving` inputs are the exception and have type `sui::transfer::Receiving<T>`. This wrap
