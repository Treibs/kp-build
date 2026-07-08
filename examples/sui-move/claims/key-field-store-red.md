---
id: key-field-store-red
statement: 'A `key` struct with a field whose type lacks `store` does not compile:
  sui 1.74.1 fails with error[E05001] ability constraint not satisfied — "The struct
  was declared with the ability ''key'' so all fields require the ability ''store''"
  (here `posts: vector<Post>` with an ability-less `Post`).'
paper: ''
supporting_passage: 'sui 1.74.1 rejects a key struct holding vector<Post> where Post
  has no abilities with exit 1, error[E05001]: the struct was declared with the ability
  ''key'' so all fields require the ability ''store''.'
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
  artifact: sui-move-fixtures/key-field-store-red
grounding: {}
judgment: {}
---

A `key` struct with a field whose type lacks `store` does not compile: sui 1.74.1 fails with error[E05001] ability constraint not satisfied — "The struct was declared with the ability 'key' so all fields require the ability 'store'" (here `posts: vector<Post>` with an ability-less `Post`).

> sui 1.74.1 rejects a key struct holding vector<Post> where Post has no abilities with exit 1, error[E05001]: the struct was declared with the ability 'key' so all fields require the ability 'store'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
