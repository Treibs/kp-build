---
id: vector-destroy-empty-doc
statement: '`destroy_empty` destroys the empty vector `v` — and aborts if `v` is not
  empty; it is the consumption path for vectors of droplet-less elements.'
paper: ''
supporting_passage: '<pre><code><b>public</b> <b>fun</b> <a href="../std/vector.md#std_vector_destroy_empty">destroy_empty</a>&lt;Element&gt;(v:
  <a href="../std/vector.md#std_vector">vector</a>&lt;Element&gt;)'
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
  evidence: '<pre><code><b>public</b> <b>fun</b> <a href="../std/vector.md#std_vector_destroy_empty">destroy_empty</a>&lt;Element&gt;(v:
    <a href="../std/vector.md#std_vector'
  checked: '2026-07-10'
execution: {}
grounding:
  source: sui-framework-docs
  supporting_passage: '<pre><code><b>public</b> <b>fun</b> <a href="../std/vector.md#std_vector_destroy_empty">destroy_empty</a>&lt;Element&gt;(v:
    <a href="../std/vector.md#std_vector">vector</a>&lt;Element&gt;)'
judgment: {}
---

`destroy_empty` destroys the empty vector `v` — and aborts if `v` is not empty; it is the consumption path for vectors of droplet-less elements.

> <pre><code><b>public</b> <b>fun</b> <a href="../std/vector.md#std_vector_destroy_empty">destroy_empty</a>&lt;Element&gt;(v: <a href="../std/vector.md#std_vector">vector</a>&lt;Element&gt;)

— *grounding verified* via doc-corpus: <pre><code><b>public</b> <b>fun</b> <a href="../std/vector.md#std_vector_destroy_empty">destroy_empty</a>&lt;Element&gt;(v: <a href="../std/vector.md#std_vector
