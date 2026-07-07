---
id: import-discipline-doc
statement: CE scripts import with `from manim import *` — the recommended way of using
  Manim, since a script typically uses many names from the Manim namespace (Scene,
  Circle, PINK, Create). The CE-vs-manimgl boundary itself is proven mechanically
  by the create-rename exec pair.
paper: ''
supporting_passage: 'This is the recommended way of using Manim, as a single script
  often uses

  multiple names from the Manim namespace. In your script, you imported and used

  ``Scene``, ``Circle``, ``PINK`` and ``Create``.'
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
  evidence: 'This is the recommended way of using Manim, as a single script often
    uses

    multiple names from the Manim namespace. In your script, you imported and used

    ``Scene'
  checked: '2026-07-06'
execution: {}
grounding:
  source: manim-tutorials
  supporting_passage: 'This is the recommended way of using Manim, as a single script
    often uses

    multiple names from the Manim namespace. In your script, you imported and used

    ``Scene``, ``Circle``, ``PINK`` and ``Create``.'
judgment: {}
---

CE scripts import with `from manim import *` — the recommended way of using Manim, since a script typically uses many names from the Manim namespace (Scene, Circle, PINK, Create). The CE-vs-manimgl boundary itself is proven mechanically by the create-rename exec pair.

> This is the recommended way of using Manim, as a single script often uses
multiple names from the Manim namespace. In your script, you imported and used
``Scene``, ``Circle``, ``PINK`` and ``Create``.

— *grounding verified* via doc-corpus: This is the recommended way of using Manim, as a single script often uses
multiple names from the Manim namespace. In your script, you imported and used
``Scene
