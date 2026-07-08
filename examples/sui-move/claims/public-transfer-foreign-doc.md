---
id: public-transfer-foreign-doc
statement: A type with the `key + store` combination can be sent onwards by anyone
  via `transfer::public_transfer` — `store` is what unlocks transfer outside the defining
  module.
paper: ''
supporting_passage: '`Gift` has a `key` and `store` combination, which means, that
  whoever owns a `Gift` can

  freely call `transfer::public_transfer` and send it to anyone else.'
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
  evidence: '`Gift` has a `key` and `store` combination, which means, that whoever
    owns a `Gift` can

    freely call `transfer::public_transfer` and send it to anyone else.'
  checked: '2026-07-08'
execution: {}
grounding:
  source: sui-move-book
  supporting_passage: '`Gift` has a `key` and `store` combination, which means, that
    whoever owns a `Gift` can

    freely call `transfer::public_transfer` and send it to anyone else.'
judgment: {}
---

A type with the `key + store` combination can be sent onwards by anyone via `transfer::public_transfer` — `store` is what unlocks transfer outside the defining module.

> `Gift` has a `key` and `store` combination, which means, that whoever owns a `Gift` can
freely call `transfer::public_transfer` and send it to anyone else.

— *grounding verified* via doc-corpus: `Gift` has a `key` and `store` combination, which means, that whoever owns a `Gift` can
freely call `transfer::public_transfer` and send it to anyone else.
