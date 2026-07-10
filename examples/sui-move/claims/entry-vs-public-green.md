---
id: entry-vs-public-green
statement: 'Plain `public fun` needs no `entry` modifier: `public fun create(ctx:
  &mut TxContext)` builds clean on sui 1.74.1; the docs (see entry-vs-public-doc)
  state a public function needs no `entry` to be callable in a transaction.'
paper: ''
supporting_passage: sui 1.74.1 builds a module exposing plain `public fun` entry points
  (no `entry` modifier) with exit 0 and no warnings.
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
  artifact: sui-move-fixtures/entry-vs-public-green
grounding: {}
judgment: {}
---

Plain `public fun` needs no `entry` modifier: `public fun create(ctx: &mut TxContext)` builds clean on sui 1.74.1; the docs (see entry-vs-public-doc) state a public function needs no `entry` to be callable in a transaction.

> sui 1.74.1 builds a module exposing plain `public fun` entry points (no `entry` modifier) with exit 0 and no warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
