---
id: config-surface-doc
statement: 'Global frame geometry lives on `config`: `config.frame_width` is the frame
  width in logical units.'
paper: ''
supporting_passage: "@property\n    def frame_width(self) -> float:\n        \"\"\"\
  Frame width in logical units (no flag).\"\"\""
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
  evidence: "@property\n    def frame_width(self) -> float:\n        \"\"\"Frame width\
    \ in logical units (no flag).\"\"\""
  checked: '2026-07-06'
execution: {}
grounding:
  source: manim-api-docs
  supporting_passage: "@property\n    def frame_width(self) -> float:\n        \"\"\
    \"Frame width in logical units (no flag).\"\"\""
judgment: {}
---

Global frame geometry lives on `config`: `config.frame_width` is the frame width in logical units.

> @property
    def frame_width(self) -> float:
        """Frame width in logical units (no flag)."""

— *grounding verified* via doc-corpus: @property
    def frame_width(self) -> float:
        """Frame width in logical units (no flag)."""
