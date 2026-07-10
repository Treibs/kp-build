---
id: events-doc
statement: 'The native signature of the emit function is `public native fun emit<T:
  copy + drop>(event: T)` — the event type must have both the `copy` and `drop` abilities.'
paper: ''
supporting_passage: '<b>public</b> <b>native</b> <b>fun</b> <a href="../sui/event.md#sui_event_emit">emit</a>&lt;T:
  <b>copy</b> + drop&gt;(<a href="../sui/event.md#sui_event">event</a>: T);'
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
  evidence: '<b>public</b> <b>native</b> <b>fun</b> <a href="../sui/event.md#sui_event_emit">emit</a>&lt;T:
    <b>copy</b> + drop&gt;(<a href="../sui/event.md#sui_event">event<'
  checked: '2026-07-10'
execution: {}
grounding:
  source: sui-framework-docs
  supporting_passage: '<b>public</b> <b>native</b> <b>fun</b> <a href="../sui/event.md#sui_event_emit">emit</a>&lt;T:
    <b>copy</b> + drop&gt;(<a href="../sui/event.md#sui_event">event</a>: T);'
judgment: {}
---

The native signature of the emit function is `public native fun emit<T: copy + drop>(event: T)` — the event type must have both the `copy` and `drop` abilities.

> <b>public</b> <b>native</b> <b>fun</b> <a href="../sui/event.md#sui_event_emit">emit</a>&lt;T: <b>copy</b> + drop&gt;(<a href="../sui/event.md#sui_event">event</a>: T);

— *grounding verified* via doc-corpus: <b>public</b> <b>native</b> <b>fun</b> <a href="../sui/event.md#sui_event_emit">emit</a>&lt;T: <b>copy</b> + drop&gt;(<a href="../sui/event.md#sui_event">event<
