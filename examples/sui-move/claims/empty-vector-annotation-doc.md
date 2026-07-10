---
id: empty-vector-annotation-doc
statement: A vector literal's type is inferred from the element type or the vector's
  usage; if it cannot be inferred, the type is specified explicitly (e.g. `vector<address>[]`).
paper: ''
supporting_passage: 'In these cases, the type of the `vector` is inferred, either
  from the element type or from the

  vector''s usage. If the type cannot be inferred, or simply for added clarity, the
  type can be

  specified explicitly:'
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
  evidence: 'In these cases, the type of the `vector` is inferred, either from the
    element type or from the

    vector''s usage. If the type cannot be inferred, or simply for add'
  checked: '2026-07-10'
execution: {}
grounding:
  source: sui-move-reference
  supporting_passage: 'In these cases, the type of the `vector` is inferred, either
    from the element type or from the

    vector''s usage. If the type cannot be inferred, or simply for added clarity,
    the type can be

    specified explicitly:'
judgment: {}
---

A vector literal's type is inferred from the element type or the vector's usage; if it cannot be inferred, the type is specified explicitly (e.g. `vector<address>[]`).

> In these cases, the type of the `vector` is inferred, either from the element type or from the
vector's usage. If the type cannot be inferred, or simply for added clarity, the type can be
specified explicitly:

— *grounding verified* via doc-corpus: In these cases, the type of the `vector` is inferred, either from the element type or from the
vector's usage. If the type cannot be inferred, or simply for add
