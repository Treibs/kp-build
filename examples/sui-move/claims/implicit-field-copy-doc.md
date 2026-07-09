---
id: implicit-field-copy-doc
statement: Reading a struct field with the dot operator (without borrowing) requires
  the field's type to have the `copy` ability.
paper: ''
supporting_passage: 'More canonically, the dot operator can be used to read fields
  of a struct without any borrowing. As

  is true with

  [dereferencing](./primitive-types/references#reading-and-writing-through-references),
  the field

  type must have the `copy` [ability](./abilities).'
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
  evidence: 'More canonically, the dot operator can be used to read fields of a struct
    without any borrowing. As

    is true with

    [dereferencing](./primitive-types/references#re'
  checked: '2026-07-09'
execution: {}
grounding:
  source: sui-move-reference
  supporting_passage: 'More canonically, the dot operator can be used to read fields
    of a struct without any borrowing. As

    is true with

    [dereferencing](./primitive-types/references#reading-and-writing-through-references),
    the field

    type must have the `copy` [ability](./abilities).'
judgment: {}
---

Reading a struct field with the dot operator (without borrowing) requires the field's type to have the `copy` ability.

> More canonically, the dot operator can be used to read fields of a struct without any borrowing. As
is true with
[dereferencing](./primitive-types/references#reading-and-writing-through-references), the field
type must have the `copy` [ability](./abilities).

— *grounding verified* via doc-corpus: More canonically, the dot operator can be used to read fields of a struct without any borrowing. As
is true with
[dereferencing](./primitive-types/references#re
