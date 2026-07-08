---
id: circle-surround-doc
statement: The CE `Circle.surround` signature is `surround(mobject, dim_to_match=0,
  stretch=False, buffer_factor=1.2)` — sizing is controlled by the multiplicative
  `buffer_factor`, not an additive buffer.
paper: ''
supporting_passage: "    def surround(\n        self,\n        mobject: Mobject,\n\
  \        dim_to_match: int = 0,\n        stretch: bool = False,\n        buffer_factor:\
  \ float = 1.2,\n    ) -> Self:\n        \"\"\"Modifies a circle so that it surrounds\
  \ a given mobject."
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
  evidence: "    def surround(\n        self,\n        mobject: Mobject,\n       \
    \ dim_to_match: int = 0,\n        stretch: bool = False,\n        buffer_factor:\
    \ float = 1.2,\n    "
  checked: '2026-07-08'
execution: {}
grounding:
  source: manim-api-docs
  supporting_passage: "    def surround(\n        self,\n        mobject: Mobject,\n\
    \        dim_to_match: int = 0,\n        stretch: bool = False,\n        buffer_factor:\
    \ float = 1.2,\n    ) -> Self:\n        \"\"\"Modifies a circle so that it surrounds\
    \ a given mobject."
judgment: {}
---

The CE `Circle.surround` signature is `surround(mobject, dim_to_match=0, stretch=False, buffer_factor=1.2)` — sizing is controlled by the multiplicative `buffer_factor`, not an additive buffer.

>     def surround(
        self,
        mobject: Mobject,
        dim_to_match: int = 0,
        stretch: bool = False,
        buffer_factor: float = 1.2,
    ) -> Self:
        """Modifies a circle so that it surrounds a given mobject.

— *grounding verified* via doc-corpus:     def surround(
        self,
        mobject: Mobject,
        dim_to_match: int = 0,
        stretch: bool = False,
        buffer_factor: float = 1.2,
