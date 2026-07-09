---
id: test-scenario-doc
statement: In test_scenario tests, shared objects are accessed with `take_shared`
  and must be returned with `return_shared` before the scenario ends. The compiler
  only enforces this discipline under `sui move build --test` (leaked take_shared
  values fail there with E06001 unused value without 'drop'); plain `sui move build`
  does not compile `#[test]` code at all (triage-observed on sui 1.74.1-8fc60f1fa966;
  see examples/sui-move-fixtures/beat-log.md).
paper: ''
supporting_passage: '[Shared objects](./../object/ownership.md#shared-state) are accessed
  using `take_shared` and must be

  returned with `return_shared`:'
claim_type: method
confidence: high
corroborated_by: []
survived_refuter: true
grounded: unchecked
verified:
  exists: true
  status: verified
  kind: grounding
  via: doc-corpus
  canonical_title: ''
  match_score: 0.0
  evidence: '[Shared objects](./../object/ownership.md#shared-state) are accessed
    using `take_shared` and must be

    returned with `return_shared`:'
  checked: '2026-07-09'
execution: {}
grounding:
  source: sui-move-book
  supporting_passage: '[Shared objects](./../object/ownership.md#shared-state) are
    accessed using `take_shared` and must be

    returned with `return_shared`:'
judgment: {}
---

In test_scenario tests, shared objects are accessed with `take_shared` and must be returned with `return_shared` before the scenario ends. The compiler only enforces this discipline under `sui move build --test` (leaked take_shared values fail there with E06001 unused value without 'drop'); plain `sui move build` does not compile `#[test]` code at all (triage-observed on sui 1.74.1-8fc60f1fa966; see examples/sui-move-fixtures/beat-log.md).

> [Shared objects](./../object/ownership.md#shared-state) are accessed using `take_shared` and must be
returned with `return_shared`:

— *grounding verified* via doc-corpus: [Shared objects](./../object/ownership.md#shared-state) are accessed using `take_shared` and must be
returned with `return_shared`:
