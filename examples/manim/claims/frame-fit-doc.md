---
id: frame-fit-doc
statement: 'The frame''s dimensions are config properties: `frame_height` returns
  the frame height in scene units.'
paper: ''
supporting_passage: "def frame_height(self) -> float:\n        \"\"\"Frame height\
  \ in logical units (no flag).\"\"\"\n        return self._d[\"frame_height\"]"
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
  evidence: "def frame_height(self) -> float:\n        \"\"\"Frame height in logical\
    \ units (no flag).\"\"\"\n        return self._d[\"frame_height\"]"
  checked: '2026-07-10'
execution: {}
grounding:
  source: manim-api-docs
  supporting_passage: "def frame_height(self) -> float:\n        \"\"\"Frame height\
    \ in logical units (no flag).\"\"\"\n        return self._d[\"frame_height\"]"
judgment: {}
---

The frame's dimensions are config properties: `frame_height` returns the frame height in scene units.

> def frame_height(self) -> float:
        """Frame height in logical units (no flag)."""
        return self._d["frame_height"]

— *grounding verified* via doc-corpus: def frame_height(self) -> float:
        """Frame height in logical units (no flag)."""
        return self._d["frame_height"]
