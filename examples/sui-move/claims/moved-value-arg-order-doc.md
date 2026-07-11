---
id: moved-value-arg-order-doc
statement: After a `move` occurs the local variable is unavailable — even if the value's
  type has the `copy` ability — so any field read must happen before the value moves.
paper: ''
supporting_passage: '`move` takes the value out of the local variable _without_ copying
  the data. After a `move` occurs,

  the local variable is unavailable, even if the value''s type has the `copy` [ability](./abilities).'
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
  evidence: '`move` takes the value out of the local variable _without_ copying the
    data. After a `move` occurs,

    the local variable is unavailable, even if the value''s type '
  checked: '2026-07-10'
execution: {}
grounding:
  source: sui-move-reference
  supporting_passage: '`move` takes the value out of the local variable _without_
    copying the data. After a `move` occurs,

    the local variable is unavailable, even if the value''s type has the `copy` [ability](./abilities).'
judgment: {}
---

After a `move` occurs the local variable is unavailable — even if the value's type has the `copy` ability — so any field read must happen before the value moves.

> `move` takes the value out of the local variable _without_ copying the data. After a `move` occurs,
the local variable is unavailable, even if the value's type has the `copy` [ability](./abilities).

— *grounding verified* via doc-corpus: `move` takes the value out of the local variable _without_ copying the data. After a `move` occurs,
the local variable is unavailable, even if the value's type
