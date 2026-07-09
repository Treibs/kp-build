---
id: while-condition-parens-red
statement: 'Rust''s paren-free loop head does not parse: `while i < n {` is rejected
  by sui 1.74.1 with error[E01002] unexpected token — "Expected ''(''". Move 2024
  requires parentheses around the `while` condition.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects `while i < n {` with exit 1, error[E01002]:
  unexpected token, Expected ''(''.'
claim_type: finding
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
  evidence: sui-move-build:red_violation cleared
  checked: '2026-07-09'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/while-condition-parens-red
grounding: {}
judgment: {}
---

Rust's paren-free loop head does not parse: `while i < n {` is rejected by sui 1.74.1 with error[E01002] unexpected token — "Expected '('". Move 2024 requires parentheses around the `while` condition.

> sui 1.74.1 rejects `while i < n {` with exit 1, error[E01002]: unexpected token, Expected '('.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
