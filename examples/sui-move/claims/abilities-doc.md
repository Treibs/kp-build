---
id: abilities-doc
statement: A struct with the `key` ability is an object, and the Sui Verifier requires
  its first field to be named `id` with type `UID`.
paper: ''
supporting_passage: 'A struct with the `key` ability is considered _an object_ and
  can be used in storage functions. The

  Sui Verifier requires the first field of the struct to be named `id` and to have
  the type `UID`.'
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
  evidence: 'A struct with the `key` ability is considered _an object_ and can be
    used in storage functions. The

    Sui Verifier requires the first field of the struct to be na'
  checked: '2026-07-06'
execution: {}
grounding:
  source: sui-move-book
  supporting_passage: 'A struct with the `key` ability is considered _an object_ and
    can be used in storage functions. The

    Sui Verifier requires the first field of the struct to be named `id` and to have
    the type `UID`.'
judgment: {}
---

A struct with the `key` ability is an object, and the Sui Verifier requires its first field to be named `id` with type `UID`.

> A struct with the `key` ability is considered _an object_ and can be used in storage functions. The
Sui Verifier requires the first field of the struct to be named `id` and to have the type `UID`.

— *grounding verified* via doc-corpus: A struct with the `key` ability is considered _an object_ and can be used in storage functions. The
Sui Verifier requires the first field of the struct to be na
