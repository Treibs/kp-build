---
id: structure-4
statement: A timed element (one carrying data-start/data-duration/data-track-index)
  must have class="clip" so the runtime controls its visibility to its scheduled time
  range instead of showing it for the whole composition.
paper: ''
supporting_passage: "<div data-composition-id=\"root\" data-width=\"1920\" data-height=\"\
  1080\">\n      <h1 id=\"hero\" class=\"clip\" data-start=\"0\" data-duration=\"\
  3\"></h1>"
claim_type: method
confidence: high
corroborated_by: []
survived_refuter: true
grounded: unchecked
verified:
  exists: true
  status: verified
  kind: execution
  via: lint
  canonical_title: ''
  match_score: 0.0
  evidence: lint:timed_element_missing_clip_class cleared
  checked: '2026-06-17'
execution:
  tool: lint
  gate_code: timed_element_missing_clip_class
  artifact: hf-kpmodel-fixtures/structure-4
---

A timed element (one carrying data-start/data-duration/data-track-index) must have class="clip" so the runtime controls its visibility to its scheduled time range instead of showing it for the whole composition.

> <div data-composition-id="root" data-width="1920" data-height="1080">
      <h1 id="hero" class="clip" data-start="0" data-duration="3"></h1>

— *execution verified* via lint: lint:timed_element_missing_clip_class cleared
