---
id: borrow-arg-alias-green
statement: 'When a call takes `&mut obj.field` together with a value read from the
  same field, the read is hoisted to a `let` before the call: `let amount = peek(&p.pot);
  consume(&mut p.pot, amount)` builds green.'
paper: ''
supporting_passage: sui 1.74.1 builds a module that hoists the field read to a `let`
  before the call holding `&mut` on the same field, with exit 0 and zero warnings.
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
  artifact: sui-move-fixtures/borrow-arg-alias-green
grounding: {}
judgment: {}
---

When a call takes `&mut obj.field` together with a value read from the same field, the read is hoisted to a `let` before the call: `let amount = peek(&p.pot); consume(&mut p.pot, amount)` builds green.

> sui 1.74.1 builds a module that hoists the field read to a `let` before the call holding `&mut` on the same field, with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
