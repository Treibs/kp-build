---
id: lag-ratio-total-doc
statement: '`AnimationGroup`''s `lag_ratio` is a per-animation overlap fraction: `lag_ratio`
  n.nn starts the next animation when nnn% of the current one has played (0.0 = all
  together). It is not a fraction of the group''s total duration — with uniform 1
  s animations, lag_ratio 0.5 means starts every 0.5 s; giving the group an explicit
  run_time rescales the individual animations to fit instead.'
paper: ''
supporting_passage: "    lag_ratio\n        Defines the delay after which the animation\
  \ is applied to submobjects. A lag_ratio of\n        ``n.nn`` means the next animation\
  \ will play when ``nnn%`` of the current animation has played.\n        Defaults\
  \ to 0.0, meaning that all animations will be played together.\n\n        This does\
  \ not influence the total runtime of the animation. Instead the runtime\n      \
  \  of individual animations is adjusted so that the complete animation has the defined\n\
  \        run time."
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
  evidence: "    lag_ratio\n        Defines the delay after which the animation is\
    \ applied to submobjects. A lag_ratio of\n        ``n.nn`` means the next animation\
    \ will play "
  checked: '2026-07-09'
execution: {}
grounding:
  source: manim-api-docs
  supporting_passage: "    lag_ratio\n        Defines the delay after which the animation\
    \ is applied to submobjects. A lag_ratio of\n        ``n.nn`` means the next animation\
    \ will play when ``nnn%`` of the current animation has played.\n        Defaults\
    \ to 0.0, meaning that all animations will be played together.\n\n        This\
    \ does not influence the total runtime of the animation. Instead the runtime\n\
    \        of individual animations is adjusted so that the complete animation has\
    \ the defined\n        run time."
judgment: {}
---

`AnimationGroup`'s `lag_ratio` is a per-animation overlap fraction: `lag_ratio` n.nn starts the next animation when nnn% of the current one has played (0.0 = all together). It is not a fraction of the group's total duration — with uniform 1 s animations, lag_ratio 0.5 means starts every 0.5 s; giving the group an explicit run_time rescales the individual animations to fit instead.

>     lag_ratio
        Defines the delay after which the animation is applied to submobjects. A lag_ratio of
        ``n.nn`` means the next animation will play when ``nnn%`` of the current animation has played.
        Defaults to 0.0, meaning that all animations will be played together.

        This does not influence the total runtime of the animation. Instead the runtime
        of individual animations is adjusted so that the complete animation has the defined
        run time.

— *grounding verified* via doc-corpus:     lag_ratio
        Defines the delay after which the animation is applied to submobjects. A lag_ratio of
        ``n.nn`` means the next animation will play
