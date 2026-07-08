# Deepening round 1 — sui-move

First run of the `/kp-deepen` loop (design: `docs/specs/2026-07-07-kp-deepen-design.md`).
Pack: `examples/sui-move/` · Oracle: pinned `sui 1.74.1-8fc60f1fa966`, plain `sui move build`.

| step | ledger | outcome |
|---|---|---|
| 1 Scope | [`territories.md`](territories.md) | 5 approved territories, exclusions recorded |
| 2 Probe | [`probe/`](probe/README.md) | 15 tasks × 2 models; haiku 7/15, sonnet 15/15 |
| 3 Triage | [`triage.md`](triage.md) | 8 failures → 5 root-cause families, 4 beat-worthy; +1 warning-tier beat |
| 4 Teach | `examples/sui-move-fixtures/` + [`beat-log.md`](../../../examples/sui-move-fixtures/beat-log.md) | 9 fixtures proven pre-commit (4 GREEN+RED pairs, 1 grounding-only GREEN) |
| 5 Rebuild | `examples/sui-move/` | 47 → 61 claims; 39/39 execution gates, 22/22 grounding |
| 6 Measure (tier 1) | [`remeasure.md`](remeasure.md) | 0/8 → 4/8 compile-pass; 0/8 taught-error recurrence — **tainted, trend only** |
| 7 Ship | this PR | tier-2 held-out effect unmeasured until next pre-registered falsification |
