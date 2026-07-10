---
id: vector-contains-by-ref-red
statement: 'Passing the element by value fails: `vector::contains(blocklist, who)`
  is rejected on sui 1.74.1 with error[E04007] — "Invalid call of ''std::vector::contains''"
  (the parameter is `&Element`). Rust''s `Vec::contains` has the same by-reference
  signature; the slip is not borrowing at the call site.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects vector::contains(blocklist, who) with exit
  1, error[E04007]: incompatible types, Invalid call of ''std::vector::contains''.'
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
  artifact: sui-move-fixtures/vector-contains-by-ref-red
grounding: {}
judgment: {}
---

Passing the element by value fails: `vector::contains(blocklist, who)` is rejected on sui 1.74.1 with error[E04007] — "Invalid call of 'std::vector::contains'" (the parameter is `&Element`). Rust's `Vec::contains` has the same by-reference signature; the slip is not borrowing at the call site.

> sui 1.74.1 rejects vector::contains(blocklist, who) with exit 1, error[E04007]: incompatible types, Invalid call of 'std::vector::contains'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
