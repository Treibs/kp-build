---
id: string-append-doc
statement: '`std::string::append` appends a string, taking the destination by mutable
  reference: `append(s: &mut String, r: String)`.'
paper: ''
supporting_passage: '<pre><code><b>public</b> <b>fun</b> <a href="../std/string.md#std_string_append">append</a>(s:
  &<b>mut</b> <a href="../std/string.md#std_string_String">std::string::String</a>,
  r: <a href="../std/string.md#std_string_String">std::string::String</a>)'
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
  evidence: '<pre><code><b>public</b> <b>fun</b> <a href="../std/string.md#std_string_append">append</a>(s:
    &<b>mut</b> <a href="../std/string.md#std_string_String">std::str'
  checked: '2026-07-09'
execution: {}
grounding:
  source: sui-framework-docs
  supporting_passage: '<pre><code><b>public</b> <b>fun</b> <a href="../std/string.md#std_string_append">append</a>(s:
    &<b>mut</b> <a href="../std/string.md#std_string_String">std::string::String</a>,
    r: <a href="../std/string.md#std_string_String">std::string::String</a>)'
judgment: {}
---

`std::string::append` appends a string, taking the destination by mutable reference: `append(s: &mut String, r: String)`.

> <pre><code><b>public</b> <b>fun</b> <a href="../std/string.md#std_string_append">append</a>(s: &<b>mut</b> <a href="../std/string.md#std_string_String">std::string::String</a>, r: <a href="../std/string.md#std_string_String">std::string::String</a>)

— *grounding verified* via doc-corpus: <pre><code><b>public</b> <b>fun</b> <a href="../std/string.md#std_string_append">append</a>(s: &<b>mut</b> <a href="../std/string.md#std_string_String">std::str
