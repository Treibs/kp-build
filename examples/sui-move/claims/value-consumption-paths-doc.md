---
id: value-consumption-paths-doc
statement: Only types with the `drop` ability may be left unconsumed; everything else
  must be used or explicitly destroyed on every control-flow path.
paper: ''
supporting_passage: 'The `drop` ability allows values of types with that ability to
  be dropped. By dropped, we mean that

  value is not transferred and is effectively destroyed as the Move program executes.
  As such, this'
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
  evidence: 'The `drop` ability allows values of types with that ability to be dropped.
    By dropped, we mean that

    value is not transferred and is effectively destroyed as the'
  checked: '2026-07-10'
execution: {}
grounding:
  source: sui-move-reference
  supporting_passage: 'The `drop` ability allows values of types with that ability
    to be dropped. By dropped, we mean that

    value is not transferred and is effectively destroyed as the Move program executes.
    As such, this'
judgment: {}
---

Only types with the `drop` ability may be left unconsumed; everything else must be used or explicitly destroyed on every control-flow path.

> The `drop` ability allows values of types with that ability to be dropped. By dropped, we mean that
value is not transferred and is effectively destroyed as the Move program executes. As such, this

— *grounding verified* via doc-corpus: The `drop` ability allows values of types with that ability to be dropped. By dropped, we mean that
value is not transferred and is effectively destroyed as the
