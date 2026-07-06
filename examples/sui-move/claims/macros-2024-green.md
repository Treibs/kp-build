---
id: macros-2024-green
statement: 'Move 2024 requires `let mut` for locals that are reassigned (`let mut
  total = 0; total = total + x;`), supports single-argument `assert!(cond)` (no abort
  code needed), and labeled loops (`''scan: loop { ... break ''scan; ... }`).'
paper: ''
supporting_passage: sui 1.74.1 builds a module using `let mut` locals, single-argument
  `assert!`, and a labeled loop with exit 0.
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
  checked: '2026-07-06'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/macros-2024-green
grounding: {}
judgment: {}
---

Move 2024 requires `let mut` for locals that are reassigned (`let mut total = 0; total = total + x;`), supports single-argument `assert!(cond)` (no abort code needed), and labeled loops (`'scan: loop { ... break 'scan; ... }`).

> sui 1.74.1 builds a module using `let mut` locals, single-argument `assert!`, and a labeled loop with exit 0.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
