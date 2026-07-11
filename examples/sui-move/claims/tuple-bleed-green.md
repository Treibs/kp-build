---
id: tuple-bleed-green
statement: Paired data that must live in a container gets a named struct with `copy,
  drop, store` as needed — `vector<Entry>` storage and `Option<Entry>` views; a bare
  tuple RETURN from a plain function stays legal.
paper: ''
supporting_passage: sui 1.74.1 builds a module storing vector<Entry> with an Option<Entry>
  view and a (u64, address) tuple-returning accessor, exit 0, zero warnings.
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
  checked: '2026-07-10'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/tuple-bleed-green
grounding: {}
judgment: {}
---

Paired data that must live in a container gets a named struct with `copy, drop, store` as needed — `vector<Entry>` storage and `Option<Entry>` views; a bare tuple RETURN from a plain function stays legal.

> sui 1.74.1 builds a module storing vector<Entry> with an Option<Entry> view and a (u64, address) tuple-returning accessor, exit 0, zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
