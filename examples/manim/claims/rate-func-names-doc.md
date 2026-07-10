---
id: rate-func-names-doc
statement: The easing functions are defined with direction+curve suffixes — e.g. `ease_out_sine(t)`.
paper: ''
supporting_passage: "def ease_out_sine(t: float) -> float:\n    val: float = np.sin((t\
  \ * np.pi) / 2)\n    return val"
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
  evidence: "def ease_out_sine(t: float) -> float:\n    val: float = np.sin((t * np.pi)\
    \ / 2)\n    return val"
  checked: '2026-07-10'
execution: {}
grounding:
  source: manim-api-docs
  supporting_passage: "def ease_out_sine(t: float) -> float:\n    val: float = np.sin((t\
    \ * np.pi) / 2)\n    return val"
judgment: {}
---

The easing functions are defined with direction+curve suffixes — e.g. `ease_out_sine(t)`.

> def ease_out_sine(t: float) -> float:
    val: float = np.sin((t * np.pi) / 2)
    return val

— *grounding verified* via doc-corpus: def ease_out_sine(t: float) -> float:
    val: float = np.sin((t * np.pi) / 2)
    return val
