---
id: while-condition-parens-green
statement: 'A `while` condition is parenthesized in Move 2024: `while (i < n) { ...
  };` builds green.'
paper: ''
supporting_passage: sui 1.74.1 builds a module whose loop is written `while (i < n)
  { ... };`, with exit 0 and zero warnings.
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
  artifact: sui-move-fixtures/while-condition-parens-green
grounding: {}
judgment: {}
---

A `while` condition is parenthesized in Move 2024: `while (i < n) { ... };` builds green.

> sui 1.74.1 builds a module whose loop is written `while (i < n) { ... };`, with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
