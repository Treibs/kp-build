---
id: value-tracker-doc
statement: '`ValueTracker` tracks real-valued parameters for animating parameter changes;
  it is not meant to be displayed, and its value changes continuously when animated
  using the `.animate` syntax.'
paper: ''
supporting_passage: "A mobject that can be used for tracking (real-valued) parameters.\n\
  \    Useful for animating parameter changes.\n\n    Not meant to be displayed. \
  \ Instead the position encodes some\n    number, often one which another animation\
  \ or continual_animation\n    uses for its update function, and by treating it as\
  \ a mobject it can\n    still be animated and manipulated just like anything else.\n\
  \n    This value changes continuously when animated using the :attr:`animate` syntax."
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
  evidence: "A mobject that can be used for tracking (real-valued) parameters.\n \
    \   Useful for animating parameter changes.\n\n    Not meant to be displayed.\
    \  Instead the posit"
  checked: '2026-07-06'
execution: {}
grounding:
  source: manim-api-docs
  supporting_passage: "A mobject that can be used for tracking (real-valued) parameters.\n\
    \    Useful for animating parameter changes.\n\n    Not meant to be displayed.\
    \  Instead the position encodes some\n    number, often one which another animation\
    \ or continual_animation\n    uses for its update function, and by treating it\
    \ as a mobject it can\n    still be animated and manipulated just like anything\
    \ else.\n\n    This value changes continuously when animated using the :attr:`animate`\
    \ syntax."
judgment: {}
---

`ValueTracker` tracks real-valued parameters for animating parameter changes; it is not meant to be displayed, and its value changes continuously when animated using the `.animate` syntax.

> A mobject that can be used for tracking (real-valued) parameters.
    Useful for animating parameter changes.

    Not meant to be displayed.  Instead the position encodes some
    number, often one which another animation or continual_animation
    uses for its update function, and by treating it as a mobject it can
    still be animated and manipulated just like anything else.

    This value changes continuously when animated using the :attr:`animate` syntax.

— *grounding verified* via doc-corpus: A mobject that can be used for tracking (real-valued) parameters.
    Useful for animating parameter changes.

    Not meant to be displayed.  Instead the posit
