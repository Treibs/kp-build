---
id: witness-naming-green
statement: 'A plain (reusable) witness must NOT be named the upper-case version of
  its module name: name it e.g. `MinterWitness has drop {}` so it can be constructed
  freely — the all-caps module name pattern is reserved for one-time witnesses.'
paper: ''
supporting_passage: sui 1.74.1 (edition 2024) builds a module `minter` whose witness
  struct `MinterWitness has drop {}` is constructed manually with exit 0.
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
  checked: '2026-07-07'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/witness-naming-green
grounding: {}
judgment: {}
---

A plain (reusable) witness must NOT be named the upper-case version of its module name: name it e.g. `MinterWitness has drop {}` so it can be constructed freely — the all-caps module name pattern is reserved for one-time witnesses.

> sui 1.74.1 (edition 2024) builds a module `minter` whose witness struct `MinterWitness has drop {}` is constructed manually with exit 0.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
