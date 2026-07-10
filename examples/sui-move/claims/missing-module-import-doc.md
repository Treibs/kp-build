---
id: missing-module-import-doc
statement: A function call names its target either through an alias (bound by a `use`
  declaration) or fully qualified; a bare module alias with no `use` binding is not
  a valid path.
paper: ''
supporting_passage: When calling a function, the name can be specified either through
  an alias or fully qualified
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
  evidence: When calling a function, the name can be specified either through an alias
    or fully qualified
  checked: '2026-07-10'
execution: {}
grounding:
  source: sui-move-reference
  supporting_passage: When calling a function, the name can be specified either through
    an alias or fully qualified
judgment: {}
---

A function call names its target either through an alias (bound by a `use` declaration) or fully qualified; a bare module alias with no `use` binding is not a valid path.

> When calling a function, the name can be specified either through an alias or fully qualified

— *grounding verified* via doc-corpus: When calling a function, the name can be specified either through an alias or fully qualified
