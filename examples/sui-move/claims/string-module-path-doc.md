---
id: string-module-path-doc
statement: '`std::string::utf8` creates a new string from a sequence of bytes and
  aborts if the bytes are not valid UTF-8 — it is a module function, called through
  the `string` module path.'
paper: ''
supporting_passage: 'Creates a new string from a sequence of bytes. Aborts if the
  bytes do

  not represent valid utf8.'
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
  evidence: 'Creates a new string from a sequence of bytes. Aborts if the bytes do

    not represent valid utf8.'
  checked: '2026-07-07'
execution: {}
grounding:
  source: sui-framework-docs
  supporting_passage: 'Creates a new string from a sequence of bytes. Aborts if the
    bytes do

    not represent valid utf8.'
judgment: {}
---

`std::string::utf8` creates a new string from a sequence of bytes and aborts if the bytes are not valid UTF-8 — it is a module function, called through the `string` module path.

> Creates a new string from a sequence of bytes. Aborts if the bytes do
not represent valid utf8.

— *grounding verified* via doc-corpus: Creates a new string from a sequence of bytes. Aborts if the bytes do
not represent valid utf8.
