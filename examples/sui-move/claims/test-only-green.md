---
id: test-only-green
statement: Mark test helpers with `#[test_only]` (e.g. `#[test_only] public fun create_for_testing(...)`);
  they are compiled only in test mode and are commonly `public` so tests in other
  modules can call them, without affecting the production API.
paper: ''
supporting_passage: sui 1.74.1 builds a module whose `#[test_only]` helpers are called
  only from `#[test]` code with exit 0.
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
  artifact: sui-move-fixtures/test-only-green
grounding: {}
judgment: {}
---

Mark test helpers with `#[test_only]` (e.g. `#[test_only] public fun create_for_testing(...)`); they are compiled only in test mode and are commonly `public` so tests in other modules can call them, without affecting the production API.

> sui 1.74.1 builds a module whose `#[test_only]` helpers are called only from `#[test]` code with exit 0.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
