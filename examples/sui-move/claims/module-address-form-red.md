---
id: module-address-form-red
statement: 'A bare `module name {` declaration (no address qualifier) is the pre-2024
  form and does not compile: sui 1.74.1 rejects it with error[E02004] invalid ''module''
  declaration — "The module does not have a specified address" — and suggests `module
  <address>::name`. Always qualify the module with its package address.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects `module fee_splitter {` with exit 1, error[E02004]:
  Invalid module declaration. The module does not have a specified address.'
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
  artifact: sui-move-fixtures/module-address-form-red
grounding: {}
judgment: {}
---

A bare `module name {` declaration (no address qualifier) is the pre-2024 form and does not compile: sui 1.74.1 rejects it with error[E02004] invalid 'module' declaration — "The module does not have a specified address" — and suggests `module <address>::name`. Always qualify the module with its package address.

> sui 1.74.1 rejects `module fee_splitter {` with exit 1, error[E02004]: Invalid module declaration. The module does not have a specified address.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
