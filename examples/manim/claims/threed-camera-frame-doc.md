---
id: threed-camera-frame-doc
statement: The ThreeDScene camera-orientation API exposes `zoom` ("The zoom factor
  of the scene."), `focal_distance`, and `gamma` as parameters of set_camera_orientation/move_camera
  — 3D camera motion is expressed through these method parameters.
paper: ''
supporting_passage: "        focal_distance\n            The focal_distance of the\
  \ Camera.\n\n        gamma\n            The rotation of the camera about the vector\
  \ from the ORIGIN to the Camera.\n\n        zoom\n            The zoom factor of\
  \ the scene."
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
  evidence: "        focal_distance\n            The focal_distance of the Camera.\n\
    \n        gamma\n            The rotation of the camera about the vector from\
    \ the ORIGIN to t"
  checked: '2026-07-08'
execution: {}
grounding:
  source: manim-api-docs
  supporting_passage: "        focal_distance\n            The focal_distance of the\
    \ Camera.\n\n        gamma\n            The rotation of the camera about the vector\
    \ from the ORIGIN to the Camera.\n\n        zoom\n            The zoom factor\
    \ of the scene."
judgment: {}
---

The ThreeDScene camera-orientation API exposes `zoom` ("The zoom factor of the scene."), `focal_distance`, and `gamma` as parameters of set_camera_orientation/move_camera — 3D camera motion is expressed through these method parameters.

>         focal_distance
            The focal_distance of the Camera.

        gamma
            The rotation of the camera about the vector from the ORIGIN to the Camera.

        zoom
            The zoom factor of the scene.

— *grounding verified* via doc-corpus:         focal_distance
            The focal_distance of the Camera.

        gamma
            The rotation of the camera about the vector from the ORIGIN to t
