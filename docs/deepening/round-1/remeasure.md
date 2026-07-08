# Round-1 tier-1 remeasure — sui-move

> **Tier-1 numbers are tainted — these tasks selected the beats. Trend signal only; headline
> numbers come from pre-registered held-out falsification (tier 2).**

**Protocol:** the 8 probe tasks claude-haiku-4-5 failed, re-run with the **deepened** pack
payload (post-merge `CONTEXT.md` + all 61 claim statements) under the identical protocol
(fresh context, `claude -p --tools ""`, mechanical extraction, arm-neutral scaffold, pinned
`sui 1.74.1-8fc60f1fa966`, plain `sui move build`). Haiku only — sonnet had no compile-tier
failures to remeasure. Per-task artifacts under `remeasure/<task>/` (same layout as `probe/`;
buildlogs ANSI-stripped and home-directory-redacted).

## Flip table

| task | before (47-claim pack) | after (61-claim pack) | taught error recurred? |
|---|---|---|---|
| dynfields-3 | FAIL E03003 `use …::{self}` | FAIL E04006 (`&UID` passed where `&mut UID` needed) | **no** — new root cause (mutability slip) |
| ptb-2 | FAIL E03003 `use …::{self}` | FAIL E03006 (`SUI` unresolved — missing `use sui::sui::SUI`) + E01002 (missing `;` after a `while` block mid-sequence) | **no** — two new root causes (missing import; statement-position syntax) |
| ptb-3 | FAIL E03003 `use …::{self}` | **PASS CLEAN** | no |
| upgrades-2 | FAIL E03003 `use …::{self}` | FAIL E04016 (`coin::from_balance` called without `ctx`) | **no** — new root cause (API arity slip) |
| upgrades-3 | FAIL E04007 TypeName/String + E02005 OTW | **PASS WARN1** (`vector::empty` deprecation — the family deferred at triage) | no |
| security-1 | FAIL E04007 TypeName/String | **PASS CLEAN** | no |
| ownership-1 | FAIL E05001 (`T: store` transferred; restated rule, not taught) | **PASS WARN1** (Lint W99001 — the family deferred at triage) | n/a (no beat taught) |
| ownership-2 | FAIL E05001 (key-struct field lacking `store`) | FAIL E05001 — but the taught rule **was applied** (`Post has store` now present); the residual error is a *different* constraint (`Post` needs `drop` where a value is discarded) | **no** — beat applied; failure moved one level deeper |

## Reading (trend only — see taint label above)

- **Compile-pass: 0/8 → 4/8** on the exact previously-failed tasks.
- **Taught-error recurrence: 0/8.** No answer reproduced any of the five taught error classes
  (E03003 `use`-`Self`, E04007 TypeName/String, `get` deprecation, E02005 OTW collision,
  E05001 key-field-`store`) — grep-verified across all 8 buildlogs. In ownership-2 the taught
  rule is visibly applied in the answer's source; the task still fails on an adjacent,
  untaught ability rule.
- **The 4 residual failures span 5 new, unrelated root causes** (mutability of a receiver,
  a missing import, statement-position `;`, API arity, `drop` on discard — ptb-2 carries
  two). These are round-2 candidates, not evidence against the round-1 beats.
- **All 4 residual warnings (2 on PASS rows: ownership-1 W99001, upgrades-3 `vector::empty`;
  2 on FAIL logs: upgrades-2 W99001, ownership-2 `vector::empty`) fall in the two families
  explicitly recorded-and-deferred at triage** (`vector::empty` deprecation; Lint W99001
  composability) — the triage ledger and the remeasure agree.

The held-out effect of the round-1 beats is **unmeasured** until the next tier-2
falsification (pre-registered, fresh tasks, base-vs-kp); nothing in this file is a headline
claim.

*Resolution (2026-07-07, added after merge): that tier-2 run happened —
[experiment 3](../../experiments/sui-compile-pass-3/), deepened pack 4/6 vs pre-deepening
2/6 compile-pass → ships under rule branch 1. Headline numbers live there, not here.*
