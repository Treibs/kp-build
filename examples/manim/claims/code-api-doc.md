---
id: code-api-doc
statement: The current Code constructor takes the source as `code_string` (the code
  string to display) or `code_file` (a path) — plus `language` for the highlighter.
paper: ''
supporting_passage: "    code_file\n        The path to the code file to display.\n\
  \    code_string\n        Alternatively, the code string to display."
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
  evidence: "    code_file\n        The path to the code file to display.\n    code_string\n\
    \        Alternatively, the code string to display."
  checked: '2026-07-07'
execution: {}
grounding:
  source: manim-api-docs
  supporting_passage: "    code_file\n        The path to the code file to display.\n\
    \    code_string\n        Alternatively, the code string to display."
judgment: {}
---

The current Code constructor takes the source as `code_string` (the code string to display) or `code_file` (a path) — plus `language` for the highlighter.

>     code_file
        The path to the code file to display.
    code_string
        Alternatively, the code string to display.

— *grounding verified* via doc-corpus:     code_file
        The path to the code file to display.
    code_string
        Alternatively, the code string to display.
