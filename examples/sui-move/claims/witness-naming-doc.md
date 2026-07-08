---
id: witness-naming-doc
statement: The one-time witness cannot be manually created and is unique per module;
  the Sui Adapter treats a type as an OTW when it has only `drop`, has no fields,
  is not generic, and is named after the module with all uppercase letters.
paper: ''
supporting_passage: 'The OTW is a special type of Witness that can be used only once.
  It cannot be manually created and

  it is guaranteed to be unique per module. Sui Adapter treats a type as an OTW if
  it follows these

  rules:


  1. Has only `drop` ability.

  2. Has no fields.

  3. Is not a generic type.

  4. Named after the module with all uppercase letters.'
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
  evidence: 'The OTW is a special type of Witness that can be used only once. It cannot
    be manually created and

    it is guaranteed to be unique per module. Sui Adapter treats '
  checked: '2026-07-07'
execution: {}
grounding:
  source: sui-move-book
  supporting_passage: 'The OTW is a special type of Witness that can be used only
    once. It cannot be manually created and

    it is guaranteed to be unique per module. Sui Adapter treats a type as an OTW
    if it follows these

    rules:


    1. Has only `drop` ability.

    2. Has no fields.

    3. Is not a generic type.

    4. Named after the module with all uppercase letters.'
judgment: {}
---

The one-time witness cannot be manually created and is unique per module; the Sui Adapter treats a type as an OTW when it has only `drop`, has no fields, is not generic, and is named after the module with all uppercase letters.

> The OTW is a special type of Witness that can be used only once. It cannot be manually created and
it is guaranteed to be unique per module. Sui Adapter treats a type as an OTW if it follows these
rules:

1. Has only `drop` ability.
2. Has no fields.
3. Is not a generic type.
4. Named after the module with all uppercase letters.

— *grounding verified* via doc-corpus: The OTW is a special type of Witness that can be used only once. It cannot be manually created and
it is guaranteed to be unique per module. Sui Adapter treats
