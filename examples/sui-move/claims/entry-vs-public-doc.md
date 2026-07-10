---
id: entry-vs-public-doc
statement: 'Never write `public entry fun`: PTBs can call any `public` function, so
  there is no reason to add `entry` to a `public` function — sui 1.74.1 flags it with
  lint W99010 (unnecessary ''entry'' on a ''public'' function) (triage-observed on
  sui 1.74.1-8fc60f1fa966; see examples/sui-move-fixtures/beat-log.md). Reserve `entry`
  for non-public functions that should be PTB-callable but not callable from other
  packages.'
paper: ''
supporting_passage: PTBs can call any `public` function and any `entry` function,
  whether private (`entry fun f()`), or `public(package)` (`public(package) entry
  fun f()`). Non-entry private and `public(package)` functions cannot be called from
  PTBs. Note that in this way, there is no reason to add `entry` to a `public` function.
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
  evidence: PTBs can call any `public` function and any `entry` function, whether
    private (`entry fun f()`), or `public(package)` (`public(package) entry fun f()`).
    Non-ent
  checked: '2026-07-10'
execution: {}
grounding:
  source: sui-docs-concepts
  supporting_passage: PTBs can call any `public` function and any `entry` function,
    whether private (`entry fun f()`), or `public(package)` (`public(package) entry
    fun f()`). Non-entry private and `public(package)` functions cannot be called
    from PTBs. Note that in this way, there is no reason to add `entry` to a `public`
    function.
judgment: {}
---

Never write `public entry fun`: PTBs can call any `public` function, so there is no reason to add `entry` to a `public` function — sui 1.74.1 flags it with lint W99010 (unnecessary 'entry' on a 'public' function) (triage-observed on sui 1.74.1-8fc60f1fa966; see examples/sui-move-fixtures/beat-log.md). Reserve `entry` for non-public functions that should be PTB-callable but not callable from other packages.

> PTBs can call any `public` function and any `entry` function, whether private (`entry fun f()`), or `public(package)` (`public(package) entry fun f()`). Non-entry private and `public(package)` functions cannot be called from PTBs. Note that in this way, there is no reason to add `entry` to a `public` function.

— *grounding verified* via doc-corpus: PTBs can call any `public` function and any `entry` function, whether private (`entry fun f()`), or `public(package)` (`public(package) entry fun f()`). Non-ent
