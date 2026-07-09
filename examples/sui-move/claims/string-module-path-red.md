---
id: string-module-path-red
statement: 'The Rust-style associated-function path `String::utf8(b"...")` does not
  parse as a function call: Move 2024 reads `Type::name` in expression position as
  enum-variant construction, and sui 1.74.1 fails with error[E03006] unexpected name
  in this position — "Invalid construction. Expected an enum". Call `string::utf8`
  (module path, lowercase) instead.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects `String::utf8(b"hello")` with exit 1, error[E03006]:
  Invalid construction. Expected an enum.'
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
  artifact: sui-move-fixtures/string-module-path-red
grounding: {}
judgment: {}
---

The Rust-style associated-function path `String::utf8(b"...")` does not parse as a function call: Move 2024 reads `Type::name` in expression position as enum-variant construction, and sui 1.74.1 fails with error[E03006] unexpected name in this position — "Invalid construction. Expected an enum". Call `string::utf8` (module path, lowercase) instead.

> sui 1.74.1 rejects `String::utf8(b"hello")` with exit 1, error[E03006]: Invalid construction. Expected an enum.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
