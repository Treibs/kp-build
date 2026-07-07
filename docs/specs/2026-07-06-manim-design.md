# manim — design spec

**Date:** 2026-07-06 · **Status:** approved design, spec under review · **Target:** `examples/manim/` + `examples/manim-fixtures/`

**Naming/versioning:** package name is `manim` (the community edition is the only maintained
line; "CE" in the name would read as a qualifier nobody uses). The package **version is the
pinned toolchain version** (`manim@0.20.1`), so "which renderer is this verified against?" is
answered by the version string itself — same convention as `sui-move@1.74.1`. A re-verify
against a newer toolchain bumps the version mechanically.

## 1. What this pack is

A verified knowledge package that makes an agent write Manim CE scenes that **render on the
current toolchain** and stay inside the current (post-0.19) API. It is the second two-verifier
pack, pairing **execution** (every mechanical claim gated by a real render inside a
digest-pinned Docker image) with **doc-grounding** (every rule anchored to a verbatim passage
from pinned official docs). It is the first **Docker-pinned** execution pack: the oracle is
`manimcommunity/manim@sha256:f18f53f2e4eaf2ea41713437d34363fb3f5cc6008b03fd798676ac0359396c3b`
(tag `v0.20.1`; Python 3.14.3, Manim 0.20.1, TeX, ffmpeg, and fonts all frozen byte-for-byte
by the digest) — a strictly stronger pin than the sui pack's TOFU'd release binary.

**Model-weakness evidence (probe, 2026-07-06, 39 renders against the pinned image):** the
weakness is real but *localized* — this pack is aimed at the measured map, not at a blanket
"models can't write Manim" claim (they mostly can):

| territory | evidence (all reproduced in the pinned container) |
|---|---|
| recently-rewritten APIs | `Code(code=...)` → `TypeError` (0.19 rewrote the `Code` API; both probe models emit the old form); `BarChart(width=, height=)` / `Axes(height=, width=)` → `TypeError` (CE wants `x_length`/`y_length`); `Table(row_labels=["R1"])` strings → `TypeError` (labels must be mobjects) |
| manimgl bleed | `Text.fix_in_frame()` → `AttributeError` (pure manimgl; CE is `add_fixed_in_frame_mobjects`); `self.camera_frame` in a plain `Scene` → `AttributeError` (CE is `MovingCameraScene` + `self.camera.frame`) |
| animation × updater semantics | animating a label whose `DecimalNumber` updater changes submobject count mid-animation → `ValueError: zip() argument 2 is longer than argument 1`; intermittent even for a strong model |
| namespace collisions | a strong model named its Scene class `MarkupText`, shadowing manim's class under `from manim import *` → `TypeError` at first use |

Probe pass rates: strong model 19/23 (~83%), small model 12/18 (~67%). Basic plotting,
`TransformMatchingTex`, 3D scenes, graphs, boolean ops, dt-updaters, and custom `Animation`
subclasses were all green on both models — beats there would teach what models already know,
so the beat plan is weighted away from them.

**Why it matters (the shareable story):** ask an AI for a Manim animation and it may write
code for a library that no longer exists — a blend of 3blue1brown's `manimgl` and pre-0.19
ManimCE. Every rule in this pack already ran through the real renderer, and every rule ships
with the broken form a model actually wrote.

**Honest scope note (must appear in the README):** for strong models on common scene types,
render-pass is near ceiling. The pack's measured value is (a) weaker/cheaper models and
(b) the four territories above, for all models. The falsification protocol (§6) tests exactly
that claim, not a broader one.

## 2. Scope declaration (depth is set here)

- **Scope: scene authoring against the pinned toolchain** — Python source that renders with
  `manim` inside the pinned image.
- **Depth: aimed, not thesis-broad.** ~16 beats weighted to the measured weakness map, plus a
  thin core-idiom spine for grounding coverage. The coverage label is relative to this
  declared aim.
- **Explicitly out of scope for v1** (planned follow-ons or non-goals, not silent gaps):
  - visual/aesthetic quality of the animation (judgment layer; a blind-panel axis is a
    natural v2 once fundamentals are falsified)
  - manimgl / 3b1b-repo authoring (different library; the pack teaches the boundary, not
    the other side)
  - interactive/OpenGL renderer specifics (`--renderer=opengl`), plugins, `manim-slides`
  - performance tuning of renders (frame budgets are a harness concern, § 5)

## 3. Verifiers exercised

| kind | oracle | what it proves |
|---|---|---|
| execution (primary) | `manim -ql --disable_caching` render inside the digest-pinned container | the idiom mechanically renders (or mechanically fails) on the pinned toolchain |
| doc-grounding (secondary) | verbatim passage in pinned local source file (offline, `--ground-verify`) | the rule is what the official docs say, not model paraphrase |

**RED/GREEN paired fixtures.** Every mechanical claim ships two scene files under
`examples/manim-fixtures/<claim-id>/`:
- `green/scene.py` — minimal scene that renders clean and demonstrates the idiom
- `red/scene.py` — the naive-from-memory counterpart; **must fail** with the pinned error
  fragment in `expected_error.txt`

The gate is two-sided and inherits the fail-closed machinery hardened in the sui pack
(PR #9): the claim-side `gate_code` is threaded to the runner and cross-checked against the
fixture-side marker **before** rendering; marker loss or mismatch fires the claim's own gate
(`red_green_mode_mismatch` / `red_gate_unverifiable`), never a vacuous pass.

**Animation-semantics constraint (probe lesson):** one measured crash class only fires *while
an animation is interpolating*. Fixture gates therefore run a real render that plays the
scene's animations — no `-s` last-frame shortcut, no `--dry_run` — and each fixture is kept
tiny (target < 15 s at `-ql`, one or two sub-second animations).

## 4. Beat plan (weighted to the measured map)

Pinned sources (vendored excerpts, license-checked, commit-pinned in `CONTEXT.md`):

- **S1 — Manim CE reference manual** (docs.manim.community; ManimCommunity/manim `docs/`) —
  ground truth for current API signatures (MIT license)
- **S2 — Manim CE changelogs** (0.19.0, 0.20.0 changelog pages in the same repo) — ground
  truth for *what changed*, anchoring the rewritten-API beats
- **S3 — Manim CE tutorials/guides** (building blocks, updaters, deep dive) — pedagogical
  anchor for the semantics beats

Beats (≈16; final list pinned during the build after each beat's RED/GREEN pair is proven
against the container):

**Part I — Rewritten APIs (each RED proven in probe)**
1. `Code`: 0.19 rewrite — `code_string=`, current attribute layout for line access
2. `Axes`/`BarChart`/plot sizing: `x_length`/`y_length`, never `width=`/`height=` kwargs
3. `Table`: row/col labels are mobjects; cell access and `get_cell` semantics
4. `BarChart` value updates: `change_bar_values` (proven green) vs rebuilding charts

**Part II — CE vs manimgl boundary**
5. Fixed-frame overlays in 3D: `add_fixed_in_frame_mobjects(title)` — `fix_in_frame` is
   manimgl and does not exist
6. Camera movement in 2D: `MovingCameraScene` + `self.camera.frame`; `self.camera_frame`
   does not exist; plain `Scene` has no movable frame
7. Import discipline: `from manim import *` (CE) vs `from manimlib import *` (manimgl);
   renamed animation classes (`ShowCreation`→`Create` family) as the boundary's fingerprint

**Part III — Animation × updater semantics**
8. Never animate a mobject that carries a live structure-changing updater (`DecimalNumber`
   digit-count changes mid-`FadeIn` → `ValueError`); detach or use `always_redraw`
9. `always_redraw` (rebuild-per-frame) as the safe pattern for live labels — proven green
   in probe on both models
10. Updater lifecycle: `add_updater`/`remove_updater` discipline around `self.play`;
    dt-updaters for simulation (proven green — spine beat anchoring the crash beats)
11. `ValueTracker` + `.animate.set_value` as the canonical driver (proven green)

**Part IV — Core spine (grounding coverage + hygiene)**
12. Scene anatomy: one `construct`, `self.play`/`self.add`/`self.wait` semantics
13. Class-naming hygiene: never name a Scene after a manim class; `from manim import *`
    makes collisions fatal at first use (proven RED in probe on a strong model)
14. Render CLI: quality flags (`-ql`/`-qm`/`-qh`), `--disable_caching`, output layout
15. `MathTex` vs `Text` vs `MarkupText`: which needs LaTeX, markup syntax that renders
16. Config surface: `config.frame_width` era vs constructor kwargs (pin exact behavior by
    experiment during build)

Every beat gets: GREEN fixture, RED fixture with expected error fragment, grounding passage
(verbatim, from the pinned source file), claim entry with `execution:` + `grounding:` blocks.

## 5. Oracle harness

- New execution tool in the verifier seam: `manim-render` (a `manim_runner` beside
  `sui_runner`). Runs the fixture's scene in the pinned container; gate = exit code +
  expected-error match for RED, with the claim-side `gate_code` cross-check (§3).
- **Toolchain pin:** image referenced **by digest** in the runner
  (`manimcommunity/manim@sha256:f18f53f2e4eaf2ea41713437d34363fb3f5cc6008b03fd798676ac0359396c3b`).
  A version guard runs `manim --version` inside the container once per process and requires
  exactly `0.20.1` (exact-match discipline from the sui `1.74.1` vs `1.74.10` collision).
  Escape hatches: `KP_BUILD_MANIM_IMAGE` (alternate image ref) and `KP_BUILD_DOCKER_BIN`
  (alternate docker binary), mirroring `KP_BUILD_SUI_BIN`.
- **Containment discipline (probe lesson):** a probe render crashed with a traceback and then
  **hung for hours** — the runner must enforce a hard wall-clock timeout at the *container*
  level (`docker run -d` + bounded `docker wait` + unconditional `docker rm -f`), never rely
  on the client exiting, and must fail closed (`render_timeout`) on expiry. `timeout(1) docker
  run` is explicitly insufficient: killing the client orphans the container.
- **Determinism note (honesty):** exit-code + error-fragment gates are deterministic under
  the digest pin. Frame-content hashing is NOT part of v1's gate (encoder nondeterminism has
  not been ruled out) — record as scope, revisit if a beat needs it.
- Execution tests skip cleanly when docker or the image is absent (same pattern as the sui
  runner's binary gating); CI does not pull the image.
- Grounding sources vendored as pinned local files (offline-only verification), MIT license,
  attribution + upstream commit recorded in `CONTEXT.md` and `examples/corpus/README.md`.

## 6. Falsification (does it help?)

- **Held-out task set, written fresh:** the probe tasks are *tainted* — they selected the
  beats — so falsification tasks must be new prompts in the same territories (e.g. "show a
  syntax-highlighted diff walkthrough", "dashboard of live-updating gauges", "camera tour of
  a mind-map", "3D plot with an on-screen legend"). 5 tasks, never appearing in the pack.
- **Pre-registered at a cited commit BEFORE any answer** (protocol from the sui pack's exp-2,
  which is now the house standard): tasks, arms, metrics, and a 3-branch ship rule, with
  "no post-hoc metric may be substituted."
- **Dual arm:** primary metric = **render-pass rate for the small model** (probe baseline
  ~67% → real headroom); secondary = render-pass rate for the strong model (probe ~83%;
  ties expected and acceptable). Ship rule drafted at pre-registration time, branch structure
  as in sui exp-2.
- Exit-code doctrine unchanged: 0 helps / 1 did not help / 3 inconclusive; 2 usage/IO.
- If the pre-registered rule does not clear, the pack does not ship. Same rule as always.

## 7. Refresh story

- Manim CE releases a few times a year (0.19.0 Jan 2025 → 0.19.1 Dec 2025 → 0.20.0 Feb 2026).
  Refresh = bump the digest pin → re-run all RED/GREEN gates. A RED that starts rendering
  means the weakness healed and the claim retires; a GREEN that breaks means the idiom moved.
  Both directions mechanical, same as sui — and the digest pin makes the *old* verification
  environment reconstructible forever, which the sui binary pin cannot promise.
- `CONTEXT.md` records image digest, tag, Python/Manim versions, and docs commits.

## 8. Deliverables

1. `examples/manim/` — the package (claims, relations, CONTEXT.md, README.md with the probe
   story and the honest scope note)
2. `examples/manim-fixtures/` — RED/GREEN scene pairs per claim + vendored pinned grounding
   sources
3. Verifier seam change: `manim-render` execution tool (`manim_runner.py`) + tests (two-sided
   gate, digest pin + version guard, container timeout fail-closed, escape hatches,
   docker-absent skips) — same test discipline as the sui runner
4. Falsification run recorded in `wikillm.json` + README before/after story
5. Corpus attribution rows in `examples/corpus/README.md` (verified against actual file
   headers, not written from memory)

## 9. Risks / open questions

- **Fixture render time**: a full RED/GREEN suite (~30 renders) at even 15 s each is ~8 min
  of wall clock per verify. Mitigations to pin in the plan: minimal `run_time`s, tiny
  resolutions if `-ql` still too slow, and parallel container lanes in the harness.
- **Error-fragment stability**: Python `TypeError`/`AttributeError` messages proved stable in
  probe and the digest pin freezes them; keep fragments minimal (exception type + key phrase)
  anyway.
- **`--disable_caching` interplay**: probe used it throughout; keep it in the gate command so
  a cached partial render can never fake a GREEN.
- **Beat 16 (config surface)**: pin exact behavior by experiment during the build — memory is
  not the arbiter, the container is.
- **Docker-in-CI**: not attempted in v1 (tests skip without the image); if wanted later, a
  weekly job pulling the image is its own decision.
- **`Text.set_text` exists in 0.20.1** (probe falsified my memory that it didn't): a reminder
  that every "does not exist" claim in Part II needs its own RED receipt, not my recall.
