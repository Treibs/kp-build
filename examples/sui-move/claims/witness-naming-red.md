---
id: witness-naming-red
statement: 'Naming a field-less `drop`-only struct the upper-case of its module name
  makes the compiler treat it as a one-time witness, so constructing it manually fails:
  sui 1.74.1 rejects `MINTER {}` in module `minter` with error[Sui E02005] invalid
  one-time witness usage — "One-time witness types cannot be created manually".'
paper: ''
supporting_passage: 'sui 1.74.1 rejects manual construction of a struct named the
  upper-case module name with exit 1, error[Sui E02005]: invalid one-time witness
  usage — One-time witness types cannot be created manually.'
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
  artifact: sui-move-fixtures/witness-naming-red
grounding: {}
judgment: {}
---

Naming a field-less `drop`-only struct the upper-case of its module name makes the compiler treat it as a one-time witness, so constructing it manually fails: sui 1.74.1 rejects `MINTER {}` in module `minter` with error[Sui E02005] invalid one-time witness usage — "One-time witness types cannot be created manually".

> sui 1.74.1 rejects manual construction of a struct named the upper-case module name with exit 1, error[Sui E02005]: invalid one-time witness usage — One-time witness types cannot be created manually.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
