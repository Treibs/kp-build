---
id: dynamic-fields-doc
statement: Sui objects can carry dynamic fields added after construction via the `sui::dynamic_field`
  module; unlike ordinary statically-declared field names, a dynamic field name can
  be any value with `copy`, `drop`, and `store` (an integer, boolean, string, ...).
paper: ''
supporting_passage: 'In addition to the fields declared in its type definition, a
  Sui object can have dynamic fields

  that can be added after the object has been constructed. Unlike ordinary field names

  (which are always statically declared identifiers) a dynamic field name can be any
  value with

  the <code><b>copy</b></code>, <code>drop</code>, and <code>store</code> abilities,
  e.g. an integer, a boolean, or a string.'
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
  evidence: 'In addition to the fields declared in its type definition, a Sui object
    can have dynamic fields

    that can be added after the object has been constructed. Unlike '
  checked: '2026-07-06'
execution: {}
grounding:
  source: sui-framework-docs
  supporting_passage: 'In addition to the fields declared in its type definition,
    a Sui object can have dynamic fields

    that can be added after the object has been constructed. Unlike ordinary field
    names

    (which are always statically declared identifiers) a dynamic field name can be
    any value with

    the <code><b>copy</b></code>, <code>drop</code>, and <code>store</code> abilities,
    e.g. an integer, a boolean, or a string.'
judgment: {}
---

Sui objects can carry dynamic fields added after construction via the `sui::dynamic_field` module; unlike ordinary statically-declared field names, a dynamic field name can be any value with `copy`, `drop`, and `store` (an integer, boolean, string, ...).

> In addition to the fields declared in its type definition, a Sui object can have dynamic fields
that can be added after the object has been constructed. Unlike ordinary field names
(which are always statically declared identifiers) a dynamic field name can be any value with
the <code><b>copy</b></code>, <code>drop</code>, and <code>store</code> abilities, e.g. an integer, a boolean, or a string.

— *grounding verified* via doc-corpus: In addition to the fields declared in its type definition, a Sui object can have dynamic fields
that can be added after the object has been constructed. Unlike
