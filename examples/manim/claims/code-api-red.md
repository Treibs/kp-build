---
id: code-api-red
statement: '`Code(code=...)` — the pre-0.19 signature both probe models write from
  memory — is rejected by the current toolchain: manim 0.20.1 fails with TypeError:
  Code.__init__() got an unexpected keyword argument ''code''. The kwarg is `code_string`
  now.'
paper: ''
supporting_passage: 'manim 0.20.1 fails the render with: Code.__init__() got an unexpected
  keyword argument ''code''.'
claim_type: finding
confidence: high
corroborated_by: []
survived_refuter: true
grounded: unchecked
verified:
  exists: true
  status: verified
  kind: execution
  via: manim-render
  canonical_title: ''
  match_score: 0.0
  evidence: manim-render:red_violation cleared
  checked: '2026-07-10'
execution:
  tool: manim-render
  gate_code: red_violation
  artifact: manim-fixtures/code-api/red
grounding: {}
judgment: {}
---

`Code(code=...)` — the pre-0.19 signature both probe models write from memory — is rejected by the current toolchain: manim 0.20.1 fails with TypeError: Code.__init__() got an unexpected keyword argument 'code'. The kwarg is `code_string` now.

> manim 0.20.1 fails the render with: Code.__init__() got an unexpected keyword argument 'code'.

— *execution verified* via manim-render: manim-render:red_violation cleared
