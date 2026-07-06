---
id: test-scenario-green
statement: 'Multi-transaction tests use `sui::test_scenario`: `let mut scenario =
  sui::test_scenario::begin(@0xA);` ... `scenario.next_tx(@0xA); let mut obj = scenario.take_shared<T>();`
  ... `sui::test_scenario::return_shared(obj); scenario.end();`. Note: plain `sui
  move build` does not compile `#[test]` code on 1.74.1 — this fixture''s test body
  was additionally verified with `sui move build --test` (exit 0).'
paper: ''
supporting_passage: 'sui 1.74.1 builds the package containing a test_scenario-based
  `#[test]` with exit 0; plain `sui move build` skips `#[test]` bodies (verified by
  planting a type error: plain build exit 0, `--test` build exit 1), and the committed
  test additionally passes `sui move build --test`.'
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
  checked: '2026-07-06'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/test-scenario-green
grounding: {}
judgment: {}
---

Multi-transaction tests use `sui::test_scenario`: `let mut scenario = sui::test_scenario::begin(@0xA);` ... `scenario.next_tx(@0xA); let mut obj = scenario.take_shared<T>();` ... `sui::test_scenario::return_shared(obj); scenario.end();`. Note: plain `sui move build` does not compile `#[test]` code on 1.74.1 — this fixture's test body was additionally verified with `sui move build --test` (exit 0).

> sui 1.74.1 builds the package containing a test_scenario-based `#[test]` with exit 0; plain `sui move build` skips `#[test]` bodies (verified by planting a type error: plain build exit 0, `--test` build exit 1), and the committed test additionally passes `sui move build --test`.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
