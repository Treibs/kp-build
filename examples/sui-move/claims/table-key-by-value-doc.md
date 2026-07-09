---
id: table-key-by-value-doc
statement: 'The `sui::table::contains` signature takes the key parameter `k: K` by
  value, with `K: copy + drop + store`.'
paper: ''
supporting_passage: '<pre><code><b>public</b> <b>fun</b> <a href="../sui/table.md#sui_table_contains">contains</a>&lt;K:
  <b>copy</b>, <a href="../sui/table.md#sui_table_drop">drop</a>, store, V: store&gt;(<a
  href="../sui/table.md#sui_table">table</a>: &<a href="../sui/table.md#sui_table_Table">sui::table::Table</a>&lt;K,
  V&gt;, k: K): bool'
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
  evidence: '<pre><code><b>public</b> <b>fun</b> <a href="../sui/table.md#sui_table_contains">contains</a>&lt;K:
    <b>copy</b>, <a href="../sui/table.md#sui_table_drop">drop</'
  checked: '2026-07-09'
execution: {}
grounding:
  source: sui-framework-docs
  supporting_passage: '<pre><code><b>public</b> <b>fun</b> <a href="../sui/table.md#sui_table_contains">contains</a>&lt;K:
    <b>copy</b>, <a href="../sui/table.md#sui_table_drop">drop</a>, store, V: store&gt;(<a
    href="../sui/table.md#sui_table">table</a>: &<a href="../sui/table.md#sui_table_Table">sui::table::Table</a>&lt;K,
    V&gt;, k: K): bool'
judgment: {}
---

The `sui::table::contains` signature takes the key parameter `k: K` by value, with `K: copy + drop + store`.

> <pre><code><b>public</b> <b>fun</b> <a href="../sui/table.md#sui_table_contains">contains</a>&lt;K: <b>copy</b>, <a href="../sui/table.md#sui_table_drop">drop</a>, store, V: store&gt;(<a href="../sui/table.md#sui_table">table</a>: &<a href="../sui/table.md#sui_table_Table">sui::table::Table</a>&lt;K, V&gt;, k: K): bool

— *grounding verified* via doc-corpus: <pre><code><b>public</b> <b>fun</b> <a href="../sui/table.md#sui_table_contains">contains</a>&lt;K: <b>copy</b>, <a href="../sui/table.md#sui_table_drop">drop</
