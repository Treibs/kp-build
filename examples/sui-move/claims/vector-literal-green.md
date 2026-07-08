---
id: vector-literal-green
statement: 'Create vectors with literals — `vector[]` for empty, `vector[e1, ...,
  en]` for elements (edition-2024 idiom). `std::vector::empty()` is deprecated on
  sui 1.74.1 and warns with warning[W04037] "The function ''std::vector::empty'' is
  deprecated: Use `vector[]` literal instead"; the literal compiles with zero warnings.'
paper: ''
supporting_passage: sui 1.74.1 (edition 2024) builds a module using `vector[]` and
  `vector[a, b]` literals with exit 0 and zero warnings.
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
  checked: '2026-07-07'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/vector-literal-green
grounding: {}
judgment: {}
---

Create vectors with literals — `vector[]` for empty, `vector[e1, ..., en]` for elements (edition-2024 idiom). `std::vector::empty()` is deprecated on sui 1.74.1 and warns with warning[W04037] "The function 'std::vector::empty' is deprecated: Use `vector[]` literal instead"; the literal compiles with zero warnings.

> sui 1.74.1 (edition 2024) builds a module using `vector[]` and `vector[a, b]` literals with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
