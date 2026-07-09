---
id: clock-doc
statement: APIs for accessing time from Move calls go through the `Clock`, a unique
  shared object created at address 0x6 during genesis — functions that need time take
  `&Clock` and call `timestamp_ms`.
paper: ''
supporting_passage: 'APIs for accessing time from move calls, via the <code><a href="../sui/clock.md#sui_clock_Clock">Clock</a></code>:
  a unique

  shared object that is created at 0x6 during genesis.'
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
  evidence: 'APIs for accessing time from move calls, via the <code><a href="../sui/clock.md#sui_clock_Clock">Clock</a></code>:
    a unique

    shared object that is created at 0x6'
  checked: '2026-07-09'
execution: {}
grounding:
  source: sui-framework-docs
  supporting_passage: 'APIs for accessing time from move calls, via the <code><a href="../sui/clock.md#sui_clock_Clock">Clock</a></code>:
    a unique

    shared object that is created at 0x6 during genesis.'
judgment: {}
---

APIs for accessing time from Move calls go through the `Clock`, a unique shared object created at address 0x6 during genesis — functions that need time take `&Clock` and call `timestamp_ms`.

> APIs for accessing time from move calls, via the <code><a href="../sui/clock.md#sui_clock_Clock">Clock</a></code>: a unique
shared object that is created at 0x6 during genesis.

— *grounding verified* via doc-corpus: APIs for accessing time from move calls, via the <code><a href="../sui/clock.md#sui_clock_Clock">Clock</a></code>: a unique
shared object that is created at 0x6
