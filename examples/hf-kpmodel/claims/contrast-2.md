---
id: contrast-2
statement: 'Large/headline text (24px+ or 19px+ bold) gets the relaxed 3:1 threshold
  but must still clear it; a grey-on-grey display headline below 3:1 (e.g. #555 on
  #3a3a3a) fails and must be brightened into the foreground family until it passes
  3:1.'
paper: ''
supporting_passage: 'On dark backgrounds: brighten the failing color until it clears
  4.5:1 (normal text) or 3:1 (large text, 24px+ or 19px+ bold) ... Stay within the
  palette family — don''t invent a new color, adjust the existing one ... Re-run `hyperframes
  validate` until clean'
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
  artifact: hf-kpmodel-fixtures/contrast-2
---

Large/headline text (24px+ or 19px+ bold) gets the relaxed 3:1 threshold but must still clear it; a grey-on-grey display headline below 3:1 (e.g. #555 on #3a3a3a) fails and must be brightened into the foreground family until it passes 3:1.

> On dark backgrounds: brighten the failing color until it clears 4.5:1 (normal text) or 3:1 (large text, 24px+ or 19px+ bold) ... Stay within the palette family — don't invent a new color, adjust the existing one ... Re-run `hyperframes validate` until clean

— *execution verified* via validate: validate:contrastFailures cleared
