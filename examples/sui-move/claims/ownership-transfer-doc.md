---
id: ownership-transfer-doc
statement: '`transfer::transfer` is internal — callable only from the module defining
  `T` with constraint `T: key` — while `transfer::public_transfer` can be called from
  any module but requires `T` to have both `key` and `store`.'
paper: ''
supporting_passage: 'In the example above, the `transfer` function can only be called
  from the module that defines the

  `T`, and has a type constraint `T: key`. While `public_transfer` - clearly indicated
  in the name -

  can be called from any module, but requires `T` to have `key` and `store`.'
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
  evidence: 'In the example above, the `transfer` function can only be called from
    the module that defines the

    `T`, and has a type constraint `T: key`. While `public_transfe'
  checked: '2026-07-07'
execution: {}
grounding:
  source: sui-move-book
  supporting_passage: 'In the example above, the `transfer` function can only be called
    from the module that defines the

    `T`, and has a type constraint `T: key`. While `public_transfer` - clearly indicated
    in the name -

    can be called from any module, but requires `T` to have `key` and `store`.'
judgment: {}
---

`transfer::transfer` is internal — callable only from the module defining `T` with constraint `T: key` — while `transfer::public_transfer` can be called from any module but requires `T` to have both `key` and `store`.

> In the example above, the `transfer` function can only be called from the module that defines the
`T`, and has a type constraint `T: key`. While `public_transfer` - clearly indicated in the name -
can be called from any module, but requires `T` to have `key` and `store`.

— *grounding verified* via doc-corpus: In the example above, the `transfer` function can only be called from the module that defines the
`T`, and has a type constraint `T: key`. While `public_transfe
