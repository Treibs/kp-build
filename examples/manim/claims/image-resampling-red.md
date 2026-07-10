---
id: image-resampling-red
statement: 'There is no PIL/scipy-style filtering kwarg on `ImageMobject`: `ImageMobject(arr,
  filter_kwargs={"order": 0})` fails on manim 0.20.1 with TypeError: Mobject.__init__()
  got an unexpected keyword argument ''filter_kwargs''. Crispness is set via `set_resampling_algorithm`,
  not a constructor kwarg.'
paper: ''
supporting_passage: 'manim 0.20.1 rejects ImageMobject(arr, filter_kwargs={"order":
  0}) with exit 1, TypeError: Mobject.__init__() got an unexpected keyword argument
  ''filter_kwargs''.'
claim_type: finding
confidence: high
corroborated_by: []
survived_refuter: true
grounded: unchecked
verified:
  exists: true
  status: verified
  kind: execution
  via: manim-render
  canonical_title: ''
  match_score: 0.0
  evidence: manim-render:red_violation cleared
  checked: '2026-07-09'
execution:
  tool: manim-render
  gate_code: red_violation
  artifact: manim-fixtures/image-resampling/red
grounding: {}
judgment: {}
---

There is no PIL/scipy-style filtering kwarg on `ImageMobject`: `ImageMobject(arr, filter_kwargs={"order": 0})` fails on manim 0.20.1 with TypeError: Mobject.__init__() got an unexpected keyword argument 'filter_kwargs'. Crispness is set via `set_resampling_algorithm`, not a constructor kwarg.

> manim 0.20.1 rejects ImageMobject(arr, filter_kwargs={"order": 0}) with exit 1, TypeError: Mobject.__init__() got an unexpected keyword argument 'filter_kwargs'.

— *execution verified* via manim-render: manim-render:red_violation cleared
