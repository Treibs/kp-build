---
id: test-only-red
statement: Non-test code calling a `#[test_only]` function does not compile — test_only
  members are filtered out of non-test builds, so sui 1.74.1 reports a plain unbound-name
  error, error[E03005] — "Unbound function 'create_for_testing' in current scope"
  (not a dedicated test_only diagnostic).
paper: ''
supporting_passage: 'sui 1.74.1 rejects a production `public fun` that calls a `#[test_only]`
  function with exit 1, error[E03005]: unbound unscoped name — the test_only member
  simply does not exist in the non-test build.'
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
  checked: '2026-07-06'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/test-only-red
grounding: {}
judgment: {}
---

Non-test code calling a `#[test_only]` function does not compile — test_only members are filtered out of non-test builds, so sui 1.74.1 reports a plain unbound-name error, error[E03005] — "Unbound function 'create_for_testing' in current scope" (not a dedicated test_only diagnostic).

> sui 1.74.1 rejects a production `public fun` that calls a `#[test_only]` function with exit 1, error[E03005]: unbound unscoped name — the test_only member simply does not exist in the non-test build.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
