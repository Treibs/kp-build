---
id: module-address-form-green
statement: 'A Move 2024 module is declared with its package address (or named address)
  and name: `module <address>::<name> { ... }` — e.g. `module my_pkg::fee_splitter
  { ... }`. The address name is bound in the package manifest (`Move.toml`), and the
  sui CLI binds the package name itself as a named address.'
paper: ''
supporting_passage: sui 1.74.1 (edition 2024) builds a module declared `module module_address_form_green::fee_splitter
  { ... }` with exit 0 and zero warnings.
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
  artifact: sui-move-fixtures/module-address-form-green
grounding: {}
judgment: {}
---

A Move 2024 module is declared with its package address (or named address) and name: `module <address>::<name> { ... }` — e.g. `module my_pkg::fee_splitter { ... }`. The address name is bound in the package manifest (`Move.toml`), and the sui CLI binds the package name itself as a named address.

> sui 1.74.1 (edition 2024) builds a module declared `module module_address_form_green::fee_splitter { ... }` with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
