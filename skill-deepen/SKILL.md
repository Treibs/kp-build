---
name: kp-deepen
description: >-
  Run one deepening round against an existing execution-verified kp-build pack: probe harder
  territories with the real pinned oracle, triage which failures reflect stale/wrong parametric
  knowledge, teach only those as fixture-proven RED/GREEN beats, rebuild, and re-measure. Use when a
  pack owner wants the pack to keep getting deeper where it measurably matters — not for building a
  new pack (that is /kp-build) and not for citation-only packs (no execution oracle to probe against).
---

# kp-deepen — `/kp-deepen <pack_dir>`

You are the orchestrator. The engine (`kp_build`) does the mechanical, deterministic part (oracle
gates, grounding, rebuild); **you do the judgment**: choosing territories, triaging failures, and
drafting beats. Design: `docs/specs/2026-07-07-kp-deepen-design.md`.

**Core thesis:** a pack helps where the model's parametric knowledge is wrong or stale, not where it
is already strong. Depth follows **measured failures**, never encyclopedic coverage.

## Preconditions (abort before any commit if unmet)

- The pack is execution-verified: its research.json has execution claims and a working runner
  (check `verify` passes on the committed pack first).
- The pinned oracle is available (e.g. the pinned `sui` binary via `KP_BUILD_SUI_BIN`, or the
  digest-pinned Docker image). If not, **abort the round** — never substitute a different toolchain
  version.
- A headless model CLI is available for fresh-context probe answers.

## The round

Work in `docs/deepening/round-N/` where N = 1 + the highest existing round. All steps below leave
their artifacts there; beat provenance goes in the existing fixture beat-log (cross-link, don't
duplicate).

### 1. Scope (human gate 1)

Read the pack's beat-log and CONTEXT.md. Propose 3–5 territories the pack has **not** probed,
biased toward corners where parametric knowledge is likely stale (recently-changed APIs, edition
drift, restriction rules). For each: one line on why it's a candidate. Get the owner's approval of
the list (an approved design/spec naming the territories counts). Record proposed + approved + what
was deliberately excluded in `territories.md`.

**Gap-seeded rounds:** when a prior held-out falsification or an earlier round has recorded
residual failure classes as round-N+1 candidates, seed the territory list from those recorded gaps
instead of a fresh brainstorm — measured failures outrank speculation (this is the skill's core
thesis applied recursively). State the seeding rule in `territories.md`, and design probe tasks to
*elicit* each class the way it actually fired (e.g. if a defect only appeared when the task left a
choice to the model, do not constrain that choice in the probe tasks).

### 2. Probe

~3 tasks per territory. Tasks must be **concrete authoring tasks** (write a module that…), not quiz
questions, and must not restate any pack fixture. Protocol per task:

- **Arm: current pack loaded** (this is deepening — residual gaps are what matter): prompt =
  task text + the standard instruction ("Answer with the <language> source only; no tools") + the
  pack payload (CONTEXT.md + all claim statements), fresh context per task.
- Dual model: the pack's falsification primary (weak model) on every task; secondary (strong model)
  on every task. Pinned model IDs.
- Save each answer verbatim; run it through the **same oracle gate the pack's fixtures use**; record
  PASS / FAIL + the observed error text in `probe/results.txt`. Layout:
  `probe/<territory>-<k>/{task.md, <model>.answer, <model>.result}`.
- Mechanical repair rule (arm-neutral, pre-declared): save the answer unchanged; gate the whole
  answer as ONE package/unit, with any scaffold (manifest, address bindings) derived mechanically
  from the answer's own declarations; no source edit. Multi-module answers stay in one gated unit
  so a failure in ANY module is observed. Write the exact rule used into `probe/README.md`
  before collecting answers.

### 3. Triage

For every FAIL, classify:

- **beat-worthy** — the failure encodes wrong/stale parametric knowledge a rule can fix (wrong API
  shape, missed restriction, edition drift). These become beats.
- **not beat-worthy** — task ambiguity, one-off carelessness, or a failure the pack *already* covers
  (the model ignored a loaded rule — record it, a rule restated is not a new rule).

`triage.md` gets a table: task / model / observed error / verdict / reason. A territory where both
models pass everything is recorded as **"model already strong — no beats"**; that is a finding, not
a failure of the round.

### 4. Teach

Per beat-worthy failure:

1. Research the corner in the pack's **pinned docs corpus first** (byte-verbatim grounding must come
   from committed corpus files).
2. Draft the GREEN fixture (the correct form compiles/renders clean) and the RED fixture (the broken
   form the model actually wrote — minimized). `expected_error.txt` is pasted from **observed oracle
   output only**, never memory.
3. Prove BOTH through the real runner **before commit**. Triaged-out RED candidates (e.g. an error
   class the pack already pins) go in the beat-log with reasons.
4. Add the claim trio to research.json (green/red/doc), indent=2; the doc claim's passage must be a
   byte-verbatim substring of a committed corpus file.

### 5. Rebuild

`kp-build build -i <research.json> -o /tmp/<pack>-rN --execute --ground-verify` must come back fully
green. Refresh the committed pack under the established merge rules: claims/, index.json,
knowledge.json copied wholesale; README.md, wikillm.json, and the CONTEXT.md pins tail are
hand-merged (falsification history is never rewritten).

### 6. Measure — tier 1 (every round)

Re-run the **exact failed probe tasks** with the deepened pack loaded (fresh context, same models,
same oracle). `remeasure.md` gets the per-task flip table (FAIL→PASS / FAIL→FAIL) and MUST carry
this label verbatim: *"Tier-1 numbers are tainted — these tasks selected the beats. Trend signal
only; headline numbers come from pre-registered held-out falsification (tier 2)."*

### 7. Ship

Branch `deepen-<pack>-round-N` → PR carrying the ledger → adversarial whole-branch review (loop
until clean) → merge commit (never squash). The PR description states claim-count deltas and links
the ledger.

## Tier 2 (not part of a round)

Every 2–3 rounds, or before tagging a pack version: a fresh pre-registered held-out falsification —
new tasks, dual model, ship rule committed **before** any answer is collected, same protocol family
as `docs/experiments/`. This is the only source of headline numbers.

## Honesty rules (non-negotiable)

- Tier-1 results are always labeled tainted; never quote them as headline gains.
- New beats are never retroactively attributed to earlier experiments; recorded experiment numbers
  stay pinned to the pack size they measured.
- RED fragments only from observed oracle output.
- A clean territory is reported, not hidden.
- Everything committed passes the standing leak gate; oracle binary paths appear as placeholders
  (`/path/to/...`), never real local paths.

## Failure handling

- Oracle unavailable / version mismatch → abort before any commit.
- A fixture that will not prove → it does not ship; no unproven beats, ever.
- Zero beat-worthy failures overall → ledger-only PR recording the null result (skip steps 4–6).
