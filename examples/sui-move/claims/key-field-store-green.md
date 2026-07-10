---
id: key-field-store-green
statement: 'Every field of a `key` struct must have `store` — including the element
  type of a vector field: a plain struct stored inside an object must be declared
  `has store` (e.g. `public struct Post has store { … }` inside `public struct Board
  has key { id: UID, posts: vector<Post> }`).'
paper: ''
supporting_passage: sui 1.74.1 (edition 2024) builds a `key` struct with a `vector<Post>`
  field where `Post has store` with exit 0.
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
  artifact: sui-move-fixtures/key-field-store-green
grounding: {}
judgment: {}
---

Every field of a `key` struct must have `store` — including the element type of a vector field: a plain struct stored inside an object must be declared `has store` (e.g. `public struct Post has store { … }` inside `public struct Board has key { id: UID, posts: vector<Post> }`).

> sui 1.74.1 (edition 2024) builds a `key` struct with a `vector<Post>` field where `Post has store` with exit 0.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
