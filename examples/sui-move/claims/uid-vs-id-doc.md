---
id: uid-vs-id-doc
statement: '`uid_to_inner(uid: &UID): ID` is the UID→ID conversion — the identity
  carried in events and tables is the copyable `ID`.'
paper: ''
supporting_passage: '<pre><code><b>public</b> <b>fun</b> <a href="../sui/object.md#sui_object_uid_to_inner">uid_to_inner</a>(uid:
  &<a href="../sui/object.md#sui_object_UID">sui::object::UID</a>): <a href="../sui/object.md#sui_object_ID">sui::object::ID</a>'
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
  evidence: '<pre><code><b>public</b> <b>fun</b> <a href="../sui/object.md#sui_object_uid_to_inner">uid_to_inner</a>(uid:
    &<a href="../sui/object.md#sui_object_UID">sui::obj'
  checked: '2026-07-10'
execution: {}
grounding:
  source: sui-framework-docs
  supporting_passage: '<pre><code><b>public</b> <b>fun</b> <a href="../sui/object.md#sui_object_uid_to_inner">uid_to_inner</a>(uid:
    &<a href="../sui/object.md#sui_object_UID">sui::object::UID</a>): <a href="../sui/object.md#sui_object_ID">sui::object::ID</a>'
judgment: {}
---

`uid_to_inner(uid: &UID): ID` is the UID→ID conversion — the identity carried in events and tables is the copyable `ID`.

> <pre><code><b>public</b> <b>fun</b> <a href="../sui/object.md#sui_object_uid_to_inner">uid_to_inner</a>(uid: &<a href="../sui/object.md#sui_object_UID">sui::object::UID</a>): <a href="../sui/object.md#sui_object_ID">sui::object::ID</a>

— *grounding verified* via doc-corpus: <pre><code><b>public</b> <b>fun</b> <a href="../sui/object.md#sui_object_uid_to_inner">uid_to_inner</a>(uid: &<a href="../sui/object.md#sui_object_UID">sui::obj
