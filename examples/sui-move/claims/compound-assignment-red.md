---
id: compound-assignment-red
statement: 'Rust''s compound assignment does not parse: `t.total += n;` is rejected
  by sui 1.74.1 with error[E01002] unexpected token — "Unexpected ''=''", "Expected
  an expression term". Move has no `+=`/`-=` operators.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects `t.total += n;` with exit 1, error[E01002]:
  unexpected token, Unexpected ''='', Expected an expression term.'
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
  checked: '2026-07-10'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/compound-assignment-red
grounding: {}
judgment: {}
---

Rust's compound assignment does not parse: `t.total += n;` is rejected by sui 1.74.1 with error[E01002] unexpected token — "Unexpected '='", "Expected an expression term". Move has no `+=`/`-=` operators.

> sui 1.74.1 rejects `t.total += n;` with exit 1, error[E01002]: unexpected token, Unexpected '=', Expected an expression term.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
