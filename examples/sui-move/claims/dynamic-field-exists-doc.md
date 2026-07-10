---
id: dynamic-field-exists-doc
statement: '`sui::dynamic_field` exposes `public fun exists<Name: copy + drop + store>(object:
  &UID, name: Name): bool` for checking whether a dynamic field with the given name
  is attached.'
paper: ''
supporting_passage: '<pre><code><b>public</b> <b>fun</b> <a href="../sui/dynamic_field.md#sui_dynamic_field_exists">exists</a>&lt;Name:
  <b>copy</b>, drop, store&gt;(<a href="../sui/object.md#sui_object">object</a>: &<a
  href="../sui/object.md#sui_object_UID">sui::object::UID</a>, name: Name): bool'
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
  evidence: '<pre><code><b>public</b> <b>fun</b> <a href="../sui/dynamic_field.md#sui_dynamic_field_exists">exists</a>&lt;Name:
    <b>copy</b>, drop, store&gt;(<a href="../sui/'
  checked: '2026-07-10'
execution: {}
grounding:
  source: sui-framework-docs
  supporting_passage: '<pre><code><b>public</b> <b>fun</b> <a href="../sui/dynamic_field.md#sui_dynamic_field_exists">exists</a>&lt;Name:
    <b>copy</b>, drop, store&gt;(<a href="../sui/object.md#sui_object">object</a>:
    &<a href="../sui/object.md#sui_object_UID">sui::object::UID</a>, name: Name):
    bool'
judgment: {}
---

`sui::dynamic_field` exposes `public fun exists<Name: copy + drop + store>(object: &UID, name: Name): bool` for checking whether a dynamic field with the given name is attached.

> <pre><code><b>public</b> <b>fun</b> <a href="../sui/dynamic_field.md#sui_dynamic_field_exists">exists</a>&lt;Name: <b>copy</b>, drop, store&gt;(<a href="../sui/object.md#sui_object">object</a>: &<a href="../sui/object.md#sui_object_UID">sui::object::UID</a>, name: Name): bool

— *grounding verified* via doc-corpus: <pre><code><b>public</b> <b>fun</b> <a href="../sui/dynamic_field.md#sui_dynamic_field_exists">exists</a>&lt;Name: <b>copy</b>, drop, store&gt;(<a href="../sui/
