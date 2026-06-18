---
id: structure-2
statement: The root composition element must declare data-start (data-start="0");
  without it the runtime cannot begin playback.
paper: ''
supporting_passage: '| `data-start`                 | Yes      | Start time (root
  composition: use `"0"`)                          |'
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
  evidence: lint:root_composition_missing_data_start cleared
  checked: '2026-06-17'
execution:
  tool: lint
  gate_code: root_composition_missing_data_start
  artifact: hf-kpmodel-fixtures/structure-2
grounding: {}
---

The root composition element must declare data-start (data-start="0"); without it the runtime cannot begin playback.

> | `data-start`                 | Yes      | Start time (root composition: use `"0"`)                          |

— *execution verified* via lint: lint:root_composition_missing_data_start cleared
