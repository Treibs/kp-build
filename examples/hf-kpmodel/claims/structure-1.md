---
id: structure-1
statement: Every GSAP timeline in a composition must be registered on window.__timelines
  keyed by the composition's data-composition-id; an unregistered timeline never plays.
paper: ''
supporting_passage: 'Register every timeline: `window.__timelines["<composition-id>"]
  = tl`  ...  Never do: 1. Forget `window.__timelines` registration'
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
  evidence: lint:gsap_timeline_not_registered cleared
  checked: '2026-06-17'
execution:
  tool: lint
  gate_code: gsap_timeline_not_registered
  artifact: hf-kpmodel-fixtures/structure-1
---

Every GSAP timeline in a composition must be registered on window.__timelines keyed by the composition's data-composition-id; an unregistered timeline never plays.

> Register every timeline: `window.__timelines["<composition-id>"] = tl`  ...  Never do: 1. Forget `window.__timelines` registration

— *execution verified* via lint: lint:gsap_timeline_not_registered cleared
