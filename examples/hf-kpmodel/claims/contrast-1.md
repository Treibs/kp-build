---
id: contrast-1
statement: 'Normal-size body text must meet WCAG AA contrast of at least 4.5:1 against
  the background pixels actually sampled behind it; sub-threshold body color (e.g.
  #777 on #0a0f17) must be brightened until it clears 4.5:1.'
paper: ''
supporting_passage: '`hyperframes validate` runs a WCAG contrast audit by default.
  It seeks to 5 timestamps, screenshots the page, samples background pixels behind
  every text element, and computes contrast ratios. Failures appear as warnings ...
  On dark backgrounds: brighten the failing color until it clears 4.5:1 (normal text)
  or 3:1 (large text, 24px+ or 19px+ bold)'
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
  artifact: hf-kpmodel-fixtures/contrast-1
grounding: {}
---

Normal-size body text must meet WCAG AA contrast of at least 4.5:1 against the background pixels actually sampled behind it; sub-threshold body color (e.g. #777 on #0a0f17) must be brightened until it clears 4.5:1.

> `hyperframes validate` runs a WCAG contrast audit by default. It seeks to 5 timestamps, screenshots the page, samples background pixels behind every text element, and computes contrast ratios. Failures appear as warnings ... On dark backgrounds: brighten the failing color until it clears 4.5:1 (normal text) or 3:1 (large text, 24px+ or 19px+ bold)

— *execution verified* via validate: validate:contrastFailures cleared
