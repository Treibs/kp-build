---
id: macros-2024-red
statement: 'Pre-2024 style reassignment of a local declared without `mut` (`let total
  = 0; ... total = total + i;`) does not compile in edition 2024: sui 1.74.1 fails
  with error[E04024] — "Invalid assignment of immutable variable".'
paper: ''
supporting_passage: 'sui 1.74.1 rejects reassignment of locals declared without `mut`
  with exit 1, error[E04024]: invalid usage of immutable variable (one error per rebound
  variable).'
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
  checked: '2026-07-07'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/macros-2024-red
grounding: {}
judgment: {}
---

Pre-2024 style reassignment of a local declared without `mut` (`let total = 0; ... total = total + i;`) does not compile in edition 2024: sui 1.74.1 fails with error[E04024] — "Invalid assignment of immutable variable".

> sui 1.74.1 rejects reassignment of locals declared without `mut` with exit 1, error[E04024]: invalid usage of immutable variable (one error per rebound variable).

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
