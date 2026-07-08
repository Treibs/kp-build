# /kp-deepen — Pack Deepening Loop (Design)

**Date:** 2026-07-07 · **Status:** approved in session · **Pilot:** `examples/sui-move`

## Purpose

A repeatable, skill-orchestrated loop that makes an existing execution-verified pack *deeper where it
measurably matters*: probe harder territories with the real oracle, teach only what the model actually
fails, prove every new rule as fixtures, and measure the gain. Answers the owner's question — "if I keep
researching this domain, does the model using the pack keep getting better?" — with numbers each round.

**Core thesis (evidence-backed):** a pack helps where the model's parametric knowledge is wrong or
stale, not where it is already strong (sonnet tied at ceiling in both shipped falsifications). Therefore
depth must follow **measured failures**, never encyclopedic coverage.

## Decisions (fixed by this design)

| decision | choice |
|---|---|
| input trigger | `/kp-deepen <pack_dir>` orchestration skill (house pattern: Claude = judgment, engine = mechanical) |
| measurement | **two-tier** — tier 1 every round (re-run failed probe tasks, labeled tainted), tier 2 every 2-3 rounds or pre-release (fresh pre-registered held-out falsification; only source of headline numbers) |
| automation level | skill-orchestrated with two human gates: territory-list approval + normal PR review |
| engine changes | **none for round 1** (probe/re-measure drive the oracles the same way the falsification experiments did); `kp-build probe --tasks <dir>` deferred until clunkiness proves it needed |
| pilot | sui-move pack, round 1 territories proposed from: PTB composition, dynamic fields, package upgrades, object-owner patterns, security idioms |

## The round (7 steps)

1. **Scope.** Orchestrator reads the pack's beat-log + CONTEXT.md, proposes 3–5 *unprobed* territories.
   Human approves the list (gate 1).
2. **Probe.** Fresh-context answers per task (~3 tasks per territory), dual model (haiku primary,
   sonnet secondary — same logic as the shipped falsifications), each answer run through the real
   pinned oracle. Prompts, answers, and per-task oracle results saved under
   `docs/deepening/round-N/probe/`.
3. **Triage.** Failures sorted *beat-worthy* (stale/wrong parametric knowledge a rule can fix) vs *not*
   (ambiguous task, carelessness, one-off). Triage table with per-failure reasons → ledger. Same
   discipline as the beat-logs' red-candidate triage.
4. **Teach.** Per beat-worthy failure: research the corner (pinned docs corpus first), draft GREEN+RED
   fixtures, prove both against the pinned oracle **before commit**, add claim trios
   (green/red/doc) with byte-verbatim grounding passages.
5. **Rebuild.** Extend research.json (indent=2), `kp-build build --execute --ground-verify`, refresh
   pack artifacts under the established merge rules (generated files copied wholesale; README /
   wikillm.json / CONTEXT.md pins tail hand-merged).
6. **Measure (tier 1).** Re-run the exact failed probe tasks with the deepened pack loaded, same
   oracle. Per-task flip table → `remeasure.md`, explicitly labeled **tainted** (probe tasks selected
   the beats; trend signal, not headline).
7. **Ship.** Branch → PR carrying the ledger → adversarial whole-branch review → merge commit.

**Tier 2** (its own session, every 2–3 rounds or before a version tag): fresh held-out tasks, ship rule
pre-registered by commit before any answer is collected — identical protocol family to
`docs/experiments/`.

## Artifacts (one new convention, no new formats)

```
docs/deepening/round-N/
  territories.md   # proposed + approved scope, with what was deliberately excluded
  probe/           # per-task: prompt, raw answer, oracle result
  triage.md        # failure → beat-worthy? → reason
  remeasure.md     # tier-1 before/after flip table (tainted label mandatory)
```

Beat provenance stays in the existing fixture beat-logs; the ledger cross-links rather than duplicates.

## Honesty rules (inherited, made explicit in the skill text)

- Tier-1 numbers are always labeled tainted; headline claims come only from tier-2 pre-registered runs.
- New beats are never retroactively attributed to earlier experiments (the PR #11 rule).
- RED fragments come only from observed oracle output, never from memory.
- A territory that probes clean is recorded as "model already strong — no beats" (a finding, not a failure).
- Committed content passes the standing leak gate; oracle binary paths appear as placeholders.

## Failure handling

- Pinned oracle unavailable → abort before any commit.
- A fixture that will not prove → does not ship (no unproven beats, ever).
- Zero beat-worthy failures across all territories → ledger-only PR recording the null result.

## Testing

Round 1 on sui-move **is** the acceptance test: ledger complete, every new beat proven, tier-1 flips
reported, PR merged through adversarial review. The skill text is then revised from what round 1
teaches (the same way /kp-build evolved).

## Out of scope (deliberate)

- Session capture (mining live working sessions for candidate beats) — a future *discovery channel*
  feeding step 3; designed separately.
- `kp-build deepen` engine subcommand — only if rounds prove mechanical enough to encode.
- Citation-only packs (mesh, strength-training) — this loop assumes an execution oracle; a
  citation-pack variant would need a different probe gate.
