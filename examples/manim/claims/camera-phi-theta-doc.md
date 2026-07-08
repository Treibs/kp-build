---
id: camera-phi-theta-doc
statement: In CE 3D camera calls `phi` is the polar angle — the angle between the
  Z axis and the camera, so `phi=0` looks straight down and `phi=90°` is side-on —
  and `theta` is the azimuthal angle that spins the camera around the Z axis. To tilt
  the view, change `phi`, not `theta` (the math-convention swap silently leaves the
  view top-down).
paper: ''
supporting_passage: "        phi\n            The polar angle i.e the angle between\
  \ Z_AXIS and Camera through ORIGIN in radians.\n\n        theta\n            The\
  \ azimuthal angle i.e the angle that spins the camera around the Z_AXIS."
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
  evidence: "        phi\n            The polar angle i.e the angle between Z_AXIS\
    \ and Camera through ORIGIN in radians.\n\n        theta\n            The azimuthal\
    \ angle i.e th"
  checked: '2026-07-08'
execution: {}
grounding:
  source: manim-api-docs
  supporting_passage: "        phi\n            The polar angle i.e the angle between\
    \ Z_AXIS and Camera through ORIGIN in radians.\n\n        theta\n            The\
    \ azimuthal angle i.e the angle that spins the camera around the Z_AXIS."
judgment: {}
---

In CE 3D camera calls `phi` is the polar angle — the angle between the Z axis and the camera, so `phi=0` looks straight down and `phi=90°` is side-on — and `theta` is the azimuthal angle that spins the camera around the Z axis. To tilt the view, change `phi`, not `theta` (the math-convention swap silently leaves the view top-down).

>         phi
            The polar angle i.e the angle between Z_AXIS and Camera through ORIGIN in radians.

        theta
            The azimuthal angle i.e the angle that spins the camera around the Z_AXIS.

— *grounding verified* via doc-corpus:         phi
            The polar angle i.e the angle between Z_AXIS and Camera through ORIGIN in radians.

        theta
            The azimuthal angle i.e th
