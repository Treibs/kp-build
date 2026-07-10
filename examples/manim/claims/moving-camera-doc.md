---
id: moving-camera-doc
statement: '`MovingCameraScene` is the scene class whose camera can be moved; its
  documented usage animates `self.camera.frame` (e.g. `self.play(self.camera.frame.animate.set(width=...))`).'
paper: ''
supporting_passage: "class ChangingCameraWidthAndRestore(MovingCameraScene):\n   \
  \     def construct(self):\n            text = Text(\"Hello World\").set_color(BLUE)\n\
  \            self.add(text)\n            self.camera.frame.save_state()\n      \
  \      self.play(self.camera.frame.animate.set(width=text.width * 1.2))"
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
  checked: '2026-07-09'
execution: {}
grounding:
  source: manim-api-docs
  supporting_passage: "class ChangingCameraWidthAndRestore(MovingCameraScene):\n \
    \       def construct(self):\n            text = Text(\"Hello World\").set_color(BLUE)\n\
    \            self.add(text)\n            self.camera.frame.save_state()\n    \
    \        self.play(self.camera.frame.animate.set(width=text.width * 1.2))"
judgment: {}
---

`MovingCameraScene` is the scene class whose camera can be moved; its documented usage animates `self.camera.frame` (e.g. `self.play(self.camera.frame.animate.set(width=...))`).

> class ChangingCameraWidthAndRestore(MovingCameraScene):
        def construct(self):
            text = Text("Hello World").set_color(BLUE)
            self.add(text)
            self.camera.frame.save_state()
            self.play(self.camera.frame.animate.set(width=text.width * 1.2))

— *grounding verified* via doc-corpus: class ChangingCameraWidthAndRestore(MovingCameraScene):
        def construct(self):
            text = Text("Hello World").set_color(BLUE)
            self.add
