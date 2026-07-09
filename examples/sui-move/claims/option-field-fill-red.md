---
id: option-field-fill-red
statement: 'Assigning to an `Option<T>` field (`slot.item = option::some(x)`) overwrites
  the field and destroys the old value, so it requires `T: drop`; when `T` lacks `drop`,
  sui 1.74.1 fails with error[E05001] ability constraint — "Invalid mutation. Mutation
  requires the ''drop'' ability as the old value is destroyed". A runtime `assert!(is_none(...))`
  guard does not help: the requirement is on the type. Use `option::fill` (or `swap`/`extract`
  first) instead.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects `slot.item = option::some(item)` where the
  element type lacks drop with exit 1, error[E05001]: Invalid mutation. Mutation requires
  the ''drop'' ability as the old value is destroyed.'
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
  checked: '2026-07-09'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/option-field-fill-red
grounding: {}
judgment: {}
---

Assigning to an `Option<T>` field (`slot.item = option::some(x)`) overwrites the field and destroys the old value, so it requires `T: drop`; when `T` lacks `drop`, sui 1.74.1 fails with error[E05001] ability constraint — "Invalid mutation. Mutation requires the 'drop' ability as the old value is destroyed". A runtime `assert!(is_none(...))` guard does not help: the requirement is on the type. Use `option::fill` (or `swap`/`extract` first) instead.

> sui 1.74.1 rejects `slot.item = option::some(item)` where the element type lacks drop with exit 1, error[E05001]: Invalid mutation. Mutation requires the 'drop' ability as the old value is destroyed.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
