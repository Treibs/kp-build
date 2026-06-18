---
id: contrast-3
statement: 'Text must remain readable when decorative layers are removed: the text
  color itself (not a low-opacity decorative glow behind it) must carry the WCAG AA
  contrast against the real background, because validate samples the background pixels
  behind each text element.'
paper: ''
supporting_passage: '**Contrast:** enforced by `hyperframes validate` (WCAG AA). Text
  must be readable with decoratives removed.'
claim_type: method
confidence: high
corroborated_by: []
survived_refuter: true
grounded: unchecked
verified:
  exists: true
  status: verified
  kind: execution
  via: validate
  canonical_title: ''
  match_score: 0.0
  evidence: validate:contrastFailures cleared
  checked: '2026-06-17'
execution:
  tool: validate
  gate_code: contrastFailures
  artifact: hf-kpmodel-fixtures/contrast-3
grounding: {}
---

Text must remain readable when decorative layers are removed: the text color itself (not a low-opacity decorative glow behind it) must carry the WCAG AA contrast against the real background, because validate samples the background pixels behind each text element.

> **Contrast:** enforced by `hyperframes validate` (WCAG AA). Text must be readable with decoratives removed.

— *execution verified* via validate: validate:contrastFailures cleared
