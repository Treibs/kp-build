---
id: borrow-arg-alias-red
statement: 'Borrowing a field inside the argument list of a call that already holds
  `&mut` on that field fails: `consume(&mut p.pot, peek(&p.pot))` is rejected by sui
  1.74.1 with error[E07001] referential transparency violated — "Field ''pot'' is
  still being mutably borrowed by this reference". Rust''s two-phase borrows allow
  this ordering; Move holds the mutable borrow across the whole argument list.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects a second borrow of a field in the argument
  list of a call holding `&mut` on that field, with exit 1, error[E07001]: referential
  transparency violated, Field ''pot'' is still being mutably borrowed by this reference.'
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
  artifact: sui-move-fixtures/borrow-arg-alias-red
grounding: {}
judgment: {}
---

Borrowing a field inside the argument list of a call that already holds `&mut` on that field fails: `consume(&mut p.pot, peek(&p.pot))` is rejected by sui 1.74.1 with error[E07001] referential transparency violated — "Field 'pot' is still being mutably borrowed by this reference". Rust's two-phase borrows allow this ordering; Move holds the mutable borrow across the whole argument list.

> sui 1.74.1 rejects a second borrow of a field in the argument list of a call holding `&mut` on that field, with exit 1, error[E07001]: referential transparency violated, Field 'pot' is still being mutably borrowed by this reference.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
