---
id: camera-distance-kwarg-doc
statement: '`set_camera_orientation`''s signature is `(phi, theta, gamma, zoom, focal_distance,
  frame_center, **kwargs)` — there is no `distance` parameter; the CE distance controls
  are `focal_distance` and `zoom`, and an unrecognized kwarg like `distance=` lands
  in `**kwargs`.'
paper: ''
supporting_passage: "    def set_camera_orientation(\n        self,\n        phi:\
  \ float | None = None,\n        theta: float | None = None,\n        gamma: float\
  \ | None = None,\n        zoom: float | None = None,\n        focal_distance: float\
  \ | None = None,\n        frame_center: Mobject | Sequence[float] | None = None,\n\
  \        **kwargs,\n    ):"
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
  evidence: "    def set_camera_orientation(\n        self,\n        phi: float |\
    \ None = None,\n        theta: float | None = None,\n        gamma: float | None\
    \ = None,\n        "
  checked: '2026-07-10'
execution: {}
grounding:
  source: manim-api-docs
  supporting_passage: "    def set_camera_orientation(\n        self,\n        phi:\
    \ float | None = None,\n        theta: float | None = None,\n        gamma: float\
    \ | None = None,\n        zoom: float | None = None,\n        focal_distance:\
    \ float | None = None,\n        frame_center: Mobject | Sequence[float] | None\
    \ = None,\n        **kwargs,\n    ):"
judgment: {}
---

`set_camera_orientation`'s signature is `(phi, theta, gamma, zoom, focal_distance, frame_center, **kwargs)` — there is no `distance` parameter; the CE distance controls are `focal_distance` and `zoom`, and an unrecognized kwarg like `distance=` lands in `**kwargs`.

>     def set_camera_orientation(
        self,
        phi: float | None = None,
        theta: float | None = None,
        gamma: float | None = None,
        zoom: float | None = None,
        focal_distance: float | None = None,
        frame_center: Mobject | Sequence[float] | None = None,
        **kwargs,
    ):

— *grounding verified* via doc-corpus:     def set_camera_orientation(
        self,
        phi: float | None = None,
        theta: float | None = None,
        gamma: float | None = None,
