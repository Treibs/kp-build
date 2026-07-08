---
id: string-append-red
statement: '`a + b` on `String` values does not compile: `+` is an integer-only built-in
  in Move (u8..u256) and there is no operator overloading; sui 1.74.1 fails with error[E04003]
  built-in operation not supported — "Invalid argument to ''+''". Use `append` for
  concatenation.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects `a + b` on std::string::String values with
  exit 1, error[E04003]: Invalid argument to ''+''.'
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
  artifact: sui-move-fixtures/string-append-red
grounding: {}
judgment: {}
---

`a + b` on `String` values does not compile: `+` is an integer-only built-in in Move (u8..u256) and there is no operator overloading; sui 1.74.1 fails with error[E04003] built-in operation not supported — "Invalid argument to '+'". Use `append` for concatenation.

> sui 1.74.1 rejects `a + b` on std::string::String values with exit 1, error[E04003]: Invalid argument to '+'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
