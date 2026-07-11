---
id: tuple-bleed-doc
statement: Tuples in Move are not runtime values — they exist only in expression and
  return positions, which is why they cannot instantiate type arguments or be stored.
paper: ''
supporting_passage: 'As mentioned in the [tuples section](./primitive-types/tuples),
  these tuple "values" do not exist as

  runtime values.'
claim_type: definition
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
  evidence: 'As mentioned in the [tuples section](./primitive-types/tuples), these
    tuple "values" do not exist as

    runtime values.'
  checked: '2026-07-10'
execution: {}
grounding:
  source: sui-move-reference
  supporting_passage: 'As mentioned in the [tuples section](./primitive-types/tuples),
    these tuple "values" do not exist as

    runtime values.'
judgment: {}
---

Tuples in Move are not runtime values — they exist only in expression and return positions, which is why they cannot instantiate type arguments or be stored.

> As mentioned in the [tuples section](./primitive-types/tuples), these tuple "values" do not exist as
runtime values.

— *grounding verified* via doc-corpus: As mentioned in the [tuples section](./primitive-types/tuples), these tuple "values" do not exist as
runtime values.
