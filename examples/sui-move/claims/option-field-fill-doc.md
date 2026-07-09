---
id: option-field-fill-doc
statement: '`std::option::fill` converts a none option to a some option by adding
  the element, and aborts if the option already holds a value — it never discards
  an existing element.'
paper: ''
supporting_passage: 'Convert the none option <code>t</code> to a some option by adding
  <code>e</code>.

  Aborts if <code>t</code> already holds a value'
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
  evidence: 'Convert the none option <code>t</code> to a some option by adding <code>e</code>.

    Aborts if <code>t</code> already holds a value'
  checked: '2026-07-09'
execution: {}
grounding:
  source: sui-framework-docs
  supporting_passage: 'Convert the none option <code>t</code> to a some option by
    adding <code>e</code>.

    Aborts if <code>t</code> already holds a value'
judgment: {}
---

`std::option::fill` converts a none option to a some option by adding the element, and aborts if the option already holds a value — it never discards an existing element.

> Convert the none option <code>t</code> to a some option by adding <code>e</code>.
Aborts if <code>t</code> already holds a value

— *grounding verified* via doc-corpus: Convert the none option <code>t</code> to a some option by adding <code>e</code>.
Aborts if <code>t</code> already holds a value
