---
id: code-fontsize-doc
statement: Code's text styling lives in the class attribute `default_paragraph_config`
  — a dict whose keys include `font`, `font_size`, `line_spacing` and `disable_ligatures`
  — overridden per instance via the `paragraph_config` argument.
paper: ''
supporting_passage: "    default_paragraph_config: dict[str, Any] = {\n        \"\
  font\": \"Monospace\",\n        \"font_size\": 24,\n        \"line_spacing\": 0.5,\n\
  \        \"disable_ligatures\": True,\n    }"
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
  evidence: "    default_paragraph_config: dict[str, Any] = {\n        \"font\": \"\
    Monospace\",\n        \"font_size\": 24,\n        \"line_spacing\": 0.5,\n   \
    \     \"disable_ligatures\":"
  checked: '2026-07-07'
execution: {}
grounding:
  source: manim-api-docs
  supporting_passage: "    default_paragraph_config: dict[str, Any] = {\n        \"\
    font\": \"Monospace\",\n        \"font_size\": 24,\n        \"line_spacing\":\
    \ 0.5,\n        \"disable_ligatures\": True,\n    }"
judgment: {}
---

Code's text styling lives in the class attribute `default_paragraph_config` — a dict whose keys include `font`, `font_size`, `line_spacing` and `disable_ligatures` — overridden per instance via the `paragraph_config` argument.

>     default_paragraph_config: dict[str, Any] = {
        "font": "Monospace",
        "font_size": 24,
        "line_spacing": 0.5,
        "disable_ligatures": True,
    }

— *grounding verified* via doc-corpus:     default_paragraph_config: dict[str, Any] = {
        "font": "Monospace",
        "font_size": 24,
        "line_spacing": 0.5,
        "disable_ligatures":
