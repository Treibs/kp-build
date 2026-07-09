---
id: block-statement-semicolon-green
statement: 'Statements in a Move block are separated by `;` — including a braced `if`
  or `while` used as a statement mid-sequence. Unlike Rust, the separator after the
  closing brace is required: `if (cond) { x = cap };` followed by the next statement.'
paper: ''
supporting_passage: sui 1.74.1 builds a module with `if (x > cap) { x = cap };` followed
  by a final expression, with exit 0 and zero warnings.
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
  artifact: sui-move-fixtures/block-statement-semicolon-green
grounding: {}
judgment: {}
---

Statements in a Move block are separated by `;` — including a braced `if` or `while` used as a statement mid-sequence. Unlike Rust, the separator after the closing brace is required: `if (cond) { x = cap };` followed by the next statement.

> sui 1.74.1 builds a module with `if (x > cap) { x = cap };` followed by a final expression, with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
