# Round-2 tier-1 remeasure — sui-move

> **Tier-1 numbers are tainted — these tasks selected the beats. Trend signal only; headline
> numbers come from pre-registered held-out falsification (tier 2).**

**Protocol:** the 8 probe tasks claude-haiku-4-5 failed, re-run with the **deepened** pack
payload (post-refresh `CONTEXT.md` + all 86 claim statements) under the identical protocol
(fresh context, `claude -p --tools ""`, mechanical extraction, arm-neutral scaffold, pinned
`sui 1.74.1-8fc60f1fa966`, plain `sui move build`). Haiku only — sonnet had no compile-tier
failures to remeasure. Per-task artifacts under `remeasure/<task>/` (same layout as `probe/`;
buildlogs ANSI-stripped and home-directory-redacted).

## Flip table

| task | before (61-claim pack) | after (86-claim pack) | taught error recurred? |
|---|---|---|---|
| modform-2 | FAIL E04007 (`contains(&name)` — table key passed by reference) | **PASS CLEAN** | no |
| modform-3 | FAIL E02004 (bare `module fee_splitter {`) | **PASS CLEAN** | no |
| optiondrop-1 | FAIL E05001 (Option-field overwrite ×1; generic transfer bound ×2) | FAIL E03006 (`create(...): Shop<T>` with no `T` on the function — generic-scoping slip) + E05001 (`public_transfer` on `T: store` without `key` — the recorded `generic-transfer-key-bound` deferral, **2nd occurrence**) | **no** — the answer uses the taught `option::fill` / extract-first idiom throughout; both residual errors are different classes |
| optiondrop-2 | FAIL E03003 (`use …::{self}`) + E05001 (Option overwrite) | **PASS CLEAN** | no |
| optiondrop-3 | FAIL E05001 (Option-field overwrite) | FAIL E05001 — but the **destructure-ignore sibling shape** (`gift: _` unpacking a non-`drop` `Option` field), not the taught overwrite; the answer uses `option::fill`/`extract` correctly everywhere else | **no** — taught shape gone; the sibling shape recorded at triage (no pack claim or fixture teaches it) fired |
| letmut-2 | FAIL E03006 (`String::utf8` path form) + E04003 ×4 (`+` on String) | **PASS CLEAN** | no |
| letmut-3 | FAIL E01002 ×2 (missing `;` after braced `if`/`while` mid-sequence) | **PASS WARN1** (W09004 unnecessary *trailing* semicolon — over-correction untidiness, exit 0) | no |
| coinlint-1 | FAIL Sui E02009 (`transfer::transfer` on foreign `Coin<SUI>`) | **PASS WARN2** (Lint W99001 + Lint W99003) | no |

## Reading (trend only — see taint label above)

- **Compile-pass: 0/8 → 6/8** on the exact previously-failed tasks.
- **Taught-error recurrence: 0/8.** No buildlog contains any of the seven taught compile-tier
  error fragments (E02004 module-address, E05001 Option-overwrite mutation, E04007 table
  `contains` by-value, E03006 `String::utf8` enum-construction, E04003 `+` on String, E01002
  missing `;`, Sui E02009 restricted transfer) — grep-verified across all 8 buildlogs. The
  E03006 and E05001 codes that appear in the two residual failures are **different shapes**
  under the same codes (generic scoping; destructure-ignore), verified by reading the logs,
  not just the codes.
- **Both residual failures were already in the ledger as deferrals/siblings:**
  `generic-transfer-key-bound` (deferred at triage with 1 answer; now ×2 — promoted to the
  top round-3 candidate) and the Option **destructure-ignore** shape (the exp-3 sibling,
  recorded in the round ledgers only — no pack claim teaches it; second round-3 candidate). One new one-off:
  the optiondrop-1 generic-scoping slip (E03006, ×1, carelessness-adjacent).
- **Warning-tier beats are grounding-only and it shows:** Lint W99001 still fires in 2 of 8
  logs (probe: 6 of 15 haiku logs) and W99003 appeared once despite not reproducing in the
  probe. A GREEN+doc beat with no RED cannot pin a lint the way an error fixture pins a
  compile class; recorded as expected behavior, not a surprise.

The held-out effect of the round-2 beats is **unmeasured** until the next tier-2
falsification (pre-registered, fresh tasks, base-vs-kp); nothing in this file is a headline
claim.
