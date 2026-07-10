---
id: while-condition-parens-doc
statement: Move loop heads parenthesize the condition — the reference's canonical
  counting loop is written `while (i < n) { ...; i = i + 1; }`.
paper: ''
supporting_passage: "macro fun n_times($n: u64, $body: |u64| -> ()) {\n    let n =\
  \ $n;\n    let mut i = 0;\n    while (i < n) {\n        $body(i);\n        i = i\
  \ + 1;\n    }"
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
  evidence: "macro fun n_times($n: u64, $body: |u64| -> ()) {\n    let n = $n;\n \
    \   let mut i = 0;\n    while (i < n) {\n        $body(i);\n        i = i + 1;\n\
    \    }"
  checked: '2026-07-10'
execution: {}
grounding:
  source: sui-move-reference
  supporting_passage: "macro fun n_times($n: u64, $body: |u64| -> ()) {\n    let n\
    \ = $n;\n    let mut i = 0;\n    while (i < n) {\n        $body(i);\n        i\
    \ = i + 1;\n    }"
judgment: {}
---

Move loop heads parenthesize the condition — the reference's canonical counting loop is written `while (i < n) { ...; i = i + 1; }`.

> macro fun n_times($n: u64, $body: |u64| -> ()) {
    let n = $n;
    let mut i = 0;
    while (i < n) {
        $body(i);
        i = i + 1;
    }

— *grounding verified* via doc-corpus: macro fun n_times($n: u64, $body: |u64| -> ()) {
    let n = $n;
    let mut i = 0;
    while (i < n) {
        $body(i);
        i = i + 1;
    }
