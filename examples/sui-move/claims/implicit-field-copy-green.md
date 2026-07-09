---
id: implicit-field-copy-green
statement: 'Moving a non-`copy` field out of a struct is done by destructuring the
  struct: `let Pouch { gem } = p; gem` builds green — the field is moved, not copied,
  and the struct is consumed in the same step.'
paper: ''
supporting_passage: sui 1.74.1 builds a module that moves a non-`copy` field out with
  `let Pouch { gem } = p`, with exit 0 and zero warnings.
claim_type: method
confidence: high
corroborated_by: []
survived_refuter: true
grounded: unchecked
verified:
  exists: true
  status: verified
  kind: execution
  via: sui-move-build
  canonical_title: ''
  match_score: 0.0
  evidence: sui-move-build:build_error cleared
  checked: '2026-07-09'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/implicit-field-copy-green
grounding: {}
judgment: {}
---

Moving a non-`copy` field out of a struct is done by destructuring the struct: `let Pouch { gem } = p; gem` builds green — the field is moved, not copied, and the struct is consumed in the same step.

> sui 1.74.1 builds a module that moves a non-`copy` field out with `let Pouch { gem } = p`, with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
