---
id: table-key-by-value-red
statement: Passing a table key by reference (`table.contains(&key)`, the Rust habit)
  fails on sui 1.74.1 with error[E04007] incompatible types — "Invalid call of 'sui::table::contains'.
  Invalid argument for parameter 'k'" (given `&std::string::String`, expected `std::string::String`).
  Pass the key by value.
paper: ''
supporting_passage: 'sui 1.74.1 rejects `names.contains(&name)` with exit 1, error[E04007]:
  Invalid call of ''sui::table::contains''. Invalid argument for parameter ''k''.'
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
  checked: '2026-07-08'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/table-key-by-value-red
grounding: {}
judgment: {}
---

Passing a table key by reference (`table.contains(&key)`, the Rust habit) fails on sui 1.74.1 with error[E04007] incompatible types — "Invalid call of 'sui::table::contains'. Invalid argument for parameter 'k'" (given `&std::string::String`, expected `std::string::String`). Pass the key by value.

> sui 1.74.1 rejects `names.contains(&name)` with exit 1, error[E04007]: Invalid call of 'sui::table::contains'. Invalid argument for parameter 'k'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
