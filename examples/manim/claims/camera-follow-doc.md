---
id: camera-follow-doc
statement: '`MovingCameraScene` exposes the camera as `self.camera.frame`, a mobject
  that can be animated and manipulated like any other — which is what makes attaching
  an updater to it the follow-shot idiom.'
paper: ''
supporting_passage: "class ChangingCameraWidthAndRestore(MovingCameraScene):\n   \
  \     def construct(self):\n            text = Text(\"Hello World\").set_color(BLUE)\n\
  \            self.add(text)\n            self.camera.frame.save_state()"
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
  evidence: "class ChangingCameraWidthAndRestore(MovingCameraScene):\n        def\
    \ construct(self):\n            text = Text(\"Hello World\").set_color(BLUE)\n\
    \            self.add"
  checked: '2026-07-10'
execution: {}
grounding:
  source: manim-api-docs
  supporting_passage: "class ChangingCameraWidthAndRestore(MovingCameraScene):\n \
    \       def construct(self):\n            text = Text(\"Hello World\").set_color(BLUE)\n\
    \            self.add(text)\n            self.camera.frame.save_state()"
judgment: {}
---

`MovingCameraScene` exposes the camera as `self.camera.frame`, a mobject that can be animated and manipulated like any other — which is what makes attaching an updater to it the follow-shot idiom.

> class ChangingCameraWidthAndRestore(MovingCameraScene):
        def construct(self):
            text = Text("Hello World").set_color(BLUE)
            self.add(text)
            self.camera.frame.save_state()

— *grounding verified* via doc-corpus: class ChangingCameraWidthAndRestore(MovingCameraScene):
        def construct(self):
            text = Text("Hello World").set_color(BLUE)
            self.add
