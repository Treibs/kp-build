---
id: destructure-ignore-red
statement: '`field: _` in a destructure is an ignore, and ignoring a value is gated
  on the `drop` ability (unlike Rust''s `_`, which drops anything): `let Crate { id:
  _ } = c` on a `UID` field fails in sui 1.74.1 with error[E05001] — "The type ''sui::object::UID''
  does not have the ability ''drop''". The same applies to any non-`drop` field, e.g.
  an `Option<Coin<SUI>>` (use `option::destroy_none` / `destroy_some`).'
paper: ''
supporting_passage: 'sui 1.74.1 rejects `let Crate { id: _ } = c` where `id: UID`,
  with exit 1, error[E05001]: ability constraint not satisfied, The type ''sui::object::UID''
  does not have the ability ''drop''.'
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
  artifact: sui-move-fixtures/destructure-ignore-red
grounding: {}
judgment: {}
---

`field: _` in a destructure is an ignore, and ignoring a value is gated on the `drop` ability (unlike Rust's `_`, which drops anything): `let Crate { id: _ } = c` on a `UID` field fails in sui 1.74.1 with error[E05001] — "The type 'sui::object::UID' does not have the ability 'drop'". The same applies to any non-`drop` field, e.g. an `Option<Coin<SUI>>` (use `option::destroy_none` / `destroy_some`).

> sui 1.74.1 rejects `let Crate { id: _ } = c` where `id: UID`, with exit 1, error[E05001]: ability constraint not satisfied, The type 'sui::object::UID' does not have the ability 'drop'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
