---
id: std-mem-swap-doc
statement: '`std::option::swap` swaps the value inside an `Option` with a provided
  one and returns the previous contents: `swap<Element>(t: &mut Option<Element>, e:
  Element): Element`.'
paper: ''
supporting_passage: '<pre><code><b>public</b> <b>fun</b> <a href="../std/option.md#std_option_swap">swap</a>&lt;Element&gt;(t:
  &<b>mut</b> <a href="../std/option.md#std_option_Option">std::option::Option</a>&lt;Element&gt;,
  e: Element): Element'
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
  evidence: '<pre><code><b>public</b> <b>fun</b> <a href="../std/option.md#std_option_swap">swap</a>&lt;Element&gt;(t:
    &<b>mut</b> <a href="../std/option.md#std_option_Optio'
  checked: '2026-07-10'
execution: {}
grounding:
  source: sui-framework-docs
  supporting_passage: '<pre><code><b>public</b> <b>fun</b> <a href="../std/option.md#std_option_swap">swap</a>&lt;Element&gt;(t:
    &<b>mut</b> <a href="../std/option.md#std_option_Option">std::option::Option</a>&lt;Element&gt;,
    e: Element): Element'
judgment: {}
---

`std::option::swap` swaps the value inside an `Option` with a provided one and returns the previous contents: `swap<Element>(t: &mut Option<Element>, e: Element): Element`.

> <pre><code><b>public</b> <b>fun</b> <a href="../std/option.md#std_option_swap">swap</a>&lt;Element&gt;(t: &<b>mut</b> <a href="../std/option.md#std_option_Option">std::option::Option</a>&lt;Element&gt;, e: Element): Element

— *grounding verified* via doc-corpus: <pre><code><b>public</b> <b>fun</b> <a href="../std/option.md#std_option_swap">swap</a>&lt;Element&gt;(t: &<b>mut</b> <a href="../std/option.md#std_option_Optio
