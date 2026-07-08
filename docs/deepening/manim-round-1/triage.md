# manim round-1 triage

Input: `probe/results.txt` (30 gated runs). Render gate: **sonnet 15/15 PASS, haiku 13/15**.
Both FAILs are haiku. Because the render gate is API-shape-only (recorded oracle limitation,
`territories.md`), every PASS answer was also **hand-inspected against its task text** for
render-blind wrongness; those observations are listed after the FAIL table and triaged with
the same beat-worthy / not-beat-worthy standard.

## Gate failures

| task | model | observed oracle error | verdict | reason |
|---|---|---|---|---|
| legacy-3 | haiku-4-5 | `TypeError: Circle.surround() got an unexpected keyword argument 'buffer'` | **beat-worthy** | Stale signature knowledge. CE `Circle.surround(mobject, dim_to_match=0, stretch=False, buffer_factor=1.2)` scales by a multiplicative `buffer_factor`; the additive `buff`/`buffer` kwarg is the manimgl/pre-CE shape. A rule pins the real signature. Note the territory's *named* traps did not fire — haiku correctly used `Create`/`FadeOut`/`Wiggle`, not `CircleIndicate`/`WiggleOutThenIn`. |
| camera3d-3 | haiku-4-5 | `TypeError: Mobject.__init__() got an unexpected keyword argument 'size'` (`Cube(size=2, …)`) | **beat-worthy** | Wrong constructor kwarg: CE `Cube` takes `side_length` (docstring: "Length of each side"). `size=` falls through `VGroup.__init__ → Mobject.__init__` and raises. |

The camera3d-3 haiku answer contains a **second, unreached** defect: `self.play(self.camera.frame.animate.scale(0.5))`
on a `ThreeDScene` — the manimgl `camera.frame` bleed that territory 4 targeted. The Cube crash
fired first, so the oracle never observed it; it is beat-worthy in its own right and its RED
fixture generates its own observed error through the real runner (per the teach rules, no
error text is written from memory). The same answer also passes `distance=8` to
`set_camera_orientation` (see render-blind note 3 below).

## Render-blind wrongness (PASS answers whose behavior contradicts the task)

1. **compose-1 / sonnet — wrong `lag_ratio` usage.** Task: five staggered fades, each
   starting when the previous is half done, total exactly 3 s. Sonnet derived
   `lag_ratio ≈ 0.111` from an invented formula (its own comment shows the intent was
   0.5-out-of-1s offsets) and passed it to a bare `self.play(*fades, ...)`. In CE,
   `play()` kwargs are set on each animation individually (pinned `scene.py`,
   `compile_animations`), so the value staggered nothing *between* the five fades —
   the committed renderlog shows one composite animation, 15 frames @ 15 fps =
   **1.0 s total**, no stagger at all, not 3 s. Haiku got the same task right
   (`AnimationGroup(..., lag_ratio=0.5)` → starts at 0/0.5/1/1.5/2 s, total 3 s —
   renderlog 45 frames). *Correction (adversarial review round 1, 2026-07-08): this
   note originally claimed "~0.111 s intervals and a ~1.44 s total" — AnimationGroup
   start-time math misapplied to a bare play call; the committed renderlog (15 frames,
   "Played 1 animations") refutes it. Verdict (WRONG) and the beat are unchanged.*
   Disclosure: the same answer contains a second, self-corrected code block (prose:
   "Wait — … Let me reason cleanly") that does reach for `AnimationGroup` — but with
   `lag_ratio=0.5/3` ≈ 0.167 (offset ÷ total-duration again), which starts each fade
   when ~17% of the previous has played, not 50%. The graded unit is the first block
   per the pre-declared rule (and it is what the oracle rendered), but the answer is
   WRONG under either block; sonnet's gap is the lag_ratio *semantics*, not the
   AnimationGroup idiom itself.
   **Beat-worthy**
   (render-blind class → ships as GREEN + doc-grounding, no RED possible: every
   `lag_ratio` value renders clean).
2. **camera3d-1 + camera3d-2 / haiku — phi/theta convention swap, twice.** camera3d-1 asked
   for "roughly 70 degrees from vertical"; haiku wrote `set_camera_orientation(phi=0,
   theta=70*PI/180)` — `phi=0` is looking straight down, `theta` only spins the azimuth.
   camera3d-2 asked for an animated top-down→side-on move; haiku animated `theta` and left
   `phi=0`, so the view stays top-down. CE's convention (docstring): **phi is the polar
   angle** (Z-axis to camera), **theta the azimuthal angle**; haiku consistently used the
   math convention (theta = polar). Sonnet used `phi` correctly in both. **Beat-worthy**
   (render-blind → GREEN + doc-grounding).
3. **camera3d-2 + camera3d-3 / haiku — manimgl `distance=` kwarg silently swallowed.** Both
   answers pass `distance=` to `set_camera_orientation`/`move_camera`. The CE signatures end
   in unused `**kwargs`, and the body only reads phi/theta/gamma/zoom/focal_distance/
   frame_center — so `distance=` is absorbed with **no error and no effect** (the CE names
   are `focal_distance` and `zoom`). The worst kind of bleed: invisible at render time.
   **Beat-worthy** (render-blind → GREEN + doc-grounding).
4. **camera3d-2 / sonnet — "side-on" rendered at phi=72°.** `move_camera(phi=PI/2.5)` is 18°
   short of side-on. Judgment-tier imprecision, not stale API knowledge: **not beat-worthy**
   (a rule cannot fix taste; noted for a future blind-judge axis).
5. **transform-1 / both models — trap did not fire.** Haiku used `Transform(square, circle)`
   and then animated `square` — correct Transform semantics (the source mobject *is* the
   on-screen morph). Sonnet used `ReplacementTransform` and animated the target. Both
   behaviorally correct; the render-blind stale-source corner this task was built around was
   simply not hit.

## Clean territories / clean corners (findings, not failures)

- **Territory 1 core (removed names, `self.play(mob.method, arg)`):** never appeared in any
  of the six legacy answers — both models write `.animate` and current-name animations
  unprompted. The one legacy failure was the *adjacent* `surround` signature. **Model
  already strong on the deleted-name surface — no beats there.**
- **Territory 2 (composition):** all six answers render; five of six are behaviorally
  correct (`AnimationGroup(..., lag_ratio=)`, nested `AnimationGroup(lag_ratio=1)`,
  `Succession(Wait(1), …)` all used competently). The single miss is note 1.
- **Territory 3 (Transform family):** clean across all six answers, render **and**
  behavior (hand-verified). `TransformMatchingTex`-on-`Text` never attempted — both models
  hand-roll letter matching or use indexed `ReplacementTransform`. **No beats.**
- **Territory 5 (updater utilities):** clean across all six answers. The manimgl
  `always`/`f_always` NameError never fired; both models hand-roll `add_updater(lambda m,
  dt: …)` + `remove_updater` and use `always_redraw` for the glued label — all behaviorally
  correct, including the suspend/resume task. Neither model ever reaches for `always_shift`
  / `always_rotate` / `turn_animation_into_updater` / `suspend_mobject_updating`, but
  hand-rolling is *correct*, so there is no measured failure to teach against. **No beats.**

## Beat list (→ teach stage)

| beat | class | source failure | ships as |
|---|---|---|---|
| `circle-surround` | execution | legacy-3 haiku (observed TypeError) | GREEN + RED + doc |
| `cube-side-length` | execution | camera3d-3 haiku (observed TypeError) | GREEN + RED + doc |
| `threed-camera-frame` | execution | camera3d-3 haiku (unreached line; RED proves its own error through the runner) | GREEN + RED + doc |
| `camera-phi-theta` | render-blind | camera3d-1/2 haiku (behavioral, twice) | GREEN + doc |
| `camera-distance-kwarg` | render-blind | camera3d-2/3 haiku (silent no-op) | GREEN + doc |
| `lag-ratio-total` | render-blind | compose-1 sonnet (wrong total duration) | GREEN + doc |

Restatement guard: `threed-camera-frame` is distinct from the shipped `fixed-frame` beat
(manimgl `fix_in_frame` → `add_fixed_in_frame_mobjects`) and from `moving-camera` (2D
`MovingCameraScene`, where `self.camera.frame` **is** the correct API — the new beat is
specifically that the 3D `ThreeDScene`/Cairo camera has no `.frame`). None of the six touch
any existing fixture's rule.

Corpus note: the committed corpus has near-zero animation/3D-camera coverage, so the doc
claims above require a corpus extension — fetched from the **same pinned commit**
(`ManimCommunity/manim` @ `1157b746c37130685e0a02d8aa0871d1f164d5f4`, the tag v0.20.1
commit already recorded in `examples/corpus/README.md`), never from a different version.
