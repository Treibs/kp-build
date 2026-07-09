---
id: events-red
statement: 'An event struct missing `copy` (e.g. declared only `has drop`) cannot
  be emitted: sui 1.74.1 fails against `event::emit<T: copy + drop>` with error[E05001]
  ability constraint not satisfied — "The type ''events_red::notify::ValueSet'' does
  not have the ability ''copy''".'
paper: ''
supporting_passage: 'sui 1.74.1 rejects `event::emit` on a struct lacking `copy` with
  exit 1, error[E05001]: ability constraint not satisfied.'
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
  artifact: sui-move-fixtures/events-red
grounding: {}
judgment: {}
---

An event struct missing `copy` (e.g. declared only `has drop`) cannot be emitted: sui 1.74.1 fails against `event::emit<T: copy + drop>` with error[E05001] ability constraint not satisfied — "The type 'events_red::notify::ValueSet' does not have the ability 'copy'".

> sui 1.74.1 rejects `event::emit` on a struct lacking `copy` with exit 1, error[E05001]: ability constraint not satisfied.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
