---
id: object-new-doc
statement: A new UID is created with the `object::new` function, which takes a mutable
  reference to `TxContext` and returns a new `UID`; the probed `object::uid_from_bytes`
  does not exist (Unbound function 'uid_from_bytes' in module 'sui::object').
paper: ''
supporting_passage: 'New UID is created with the `object::new` function. It takes
  a mutable reference to `TxContext`, and

  returns a new `UID`.'
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
  evidence: 'New UID is created with the `object::new` function. It takes a mutable
    reference to `TxContext`, and

    returns a new `UID`.'
  checked: '2026-07-08'
execution: {}
grounding:
  source: sui-move-book
  supporting_passage: 'New UID is created with the `object::new` function. It takes
    a mutable reference to `TxContext`, and

    returns a new `UID`.'
judgment: {}
---

A new UID is created with the `object::new` function, which takes a mutable reference to `TxContext` and returns a new `UID`; the probed `object::uid_from_bytes` does not exist (Unbound function 'uid_from_bytes' in module 'sui::object').

> New UID is created with the `object::new` function. It takes a mutable reference to `TxContext`, and
returns a new `UID`.

— *grounding verified* via doc-corpus: New UID is created with the `object::new` function. It takes a mutable reference to `TxContext`, and
returns a new `UID`.
