---
id: animate-live-updater-red
statement: 'Never animate a mobject that carries a live structure-changing updater:
  `self.play(counter.animate.shift(...), tracker.animate.set_value(100))`, where counter''s
  updater changes the DecimalNumber''s digit count, crashes mid-interpolation on manim
  0.20.1 with ValueError: zip() argument 2 is longer than argument 1 — and on 0.20.1
  this crash additionally strands the SceneFileWriter''s non-daemon writer thread,
  so a bare render of the naive form hangs forever after the traceback instead of
  exiting. Detach the updater first (updater-detach) or rebuild per frame with always_redraw.'
paper: ''
supporting_passage: 'manim 0.20.1 fails the render with: ValueError: zip() argument
  2 is longer than argument 1. The committed fixture releases the stranded writer
  thread with the writer''s own sentinel and re-raises so the container exits 1 in
  bounded time; a bare render of the naive form prints the same traceback and then
  hangs (non-daemon writer_thread blocked on queue.get).'
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
  checked: '2026-07-06'
execution:
  tool: manim-render
  gate_code: red_violation
  artifact: manim-fixtures/animate-live-updater/red
grounding: {}
judgment: {}
---

Never animate a mobject that carries a live structure-changing updater: `self.play(counter.animate.shift(...), tracker.animate.set_value(100))`, where counter's updater changes the DecimalNumber's digit count, crashes mid-interpolation on manim 0.20.1 with ValueError: zip() argument 2 is longer than argument 1 — and on 0.20.1 this crash additionally strands the SceneFileWriter's non-daemon writer thread, so a bare render of the naive form hangs forever after the traceback instead of exiting. Detach the updater first (updater-detach) or rebuild per frame with always_redraw.

> manim 0.20.1 fails the render with: ValueError: zip() argument 2 is longer than argument 1. The committed fixture releases the stranded writer thread with the writer's own sentinel and re-raises so the container exits 1 in bounded time; a bare render of the naive form prints the same traceback and then hangs (non-daemon writer_thread blocked on queue.get).

— *execution verified* via manim-render: manim-render:red_violation cleared
