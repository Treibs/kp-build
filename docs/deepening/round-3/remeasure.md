# Round-3 tier-1 remeasure — sui-move

> **Tier-1 numbers are tainted — these tasks selected the beats. Trend signal only; headline
> numbers come from pre-registered held-out falsification (tier 2).**

**Protocol:** the 6 valid failed probe runs (5 haiku, 1 sonnet; import-3 was VOID at triage —
task-authoring defect — and is not remeasured), re-run with the **deepened** pack payload
(post-refresh `CONTEXT.md` + all 98 claim statements) under the identical protocol (fresh
context, `claude -p --tools ""`, mechanical extraction, arm-neutral scaffold, pinned
`sui 1.74.1-8fc60f1fa966`, plain `sui move build`). Per-task artifacts under
`remeasure/<task>/` (same layout as `probe/`; buildlogs ANSI-stripped and
home-directory-redacted).

## Flip table

| task / model | before (86-claim pack) | after (98-claim pack) | taught error recurred? |
|---|---|---|---|
| modimp-2 / haiku | FAIL E03006 (`event::emit` ×3 with no `use sui::event`) | FAIL E01002 (`fun create(...) -> Beacon` — Rust return-arrow syntax; parse error) | **no** — the answer now carries `use sui::event;` and every `event::emit` call would resolve; the residual is a **new class** (`rust-return-arrow`, ×1) |
| destr-2 / haiku | FAIL E05001 (`reward: _` ignoring a non-`drop` `Option<Coin<SUI>>`) | **PASS CLEAN** | no — the answer binds `reward` by name and threads it out via `option::extract`/`destroy_some` |
| destr-3 / haiku | FAIL E05001 (`id: _` ignoring `UID`) + Sui E01001 | FAIL Sui E01001 only (UID captured from an old object reused in a new `Snake { id: snake_id, ... }` construction) | **no** — the taught E05001 shape is gone; the residual is the `uid-reuse` class **deferred at triage with 1 answer; now ×2 → promoted round-4 candidate** |
| destr-3 / sonnet | FAIL E03002 (`use std::mem;` + `mem::replace` — Rust bleed) | FAIL E03002 — same `std-mem-replace` shape (**deferred at triage with 1 answer; now ×2 → promoted round-4 candidate**), plus downstream E03006 and Sui E02009 cascades | **needs the log, not the code:** Sui E02009 *is* a taught code (`public-transfer-foreign`), but here `Skin` is defined in the calling module — `transfer::transfer` is legal there. The compiler flags it only because `mem::replace` is unbound, so `old_skin`'s type collapses to `_` ("not declared in the current module"). Classified downstream of the `std-mem-replace` root cause, **not** a recurrence of the taught foreign-transfer shape |
| import-2 / haiku | FAIL E05001 ×2 (`let deposit = reservation.deposit;` implicit field copy) + E06001 ×2 + E01002 | FAIL E03003 ×2 + E04016 — **three independent root causes**: (1) `use sui::coin::{Coin, SUI}` (`SUI` lives in `sui::sui`, not `sui::coin`); (2) `use std::option::{self, Option}` (lowercase `self` in a group import); (3) `tips: sui::coin::zero()` — a fully-qualified call missing the required `ctx` argument (E04016 "The call expected 1 argument(s) but got 0"), independent of both unbound names. The E03006 ×3 are cascades of the unbound names | **round-3 taught classes: no** — zero implicit-copy/E05001 hits, and the round-2 taught E01002 semicolon shape (which recurred in the probe) is also gone. **But the second E03003 is the round-1 taught `use-self` class recurring under the loaded 98-claim pack** (the pack's `use-self` rule states exactly this defect) — a loaded rule ignored, recorded not re-taught. Root cause (1) is an **on-target `wrong-module-import` shape** — the territory-3 class the probe failed to elicit (`SUI-import-path`, exp-4's name for it). Root cause (3) is a genuinely new class (`api-arity-missing-ctx`, ×1 — ledger entry below) |
| generic-3 / haiku | FAIL E04024 (`relay: Relay<T>` mutated without `mut`) | FAIL E05001 ×2 (`Relay<T> has key` requires `T: store` for the phantom-less field / transfer) | **no** — the answer now writes `pass<T>(mut relay: Relay<T>, ...)`: the taught `param-mut` fix applied. The residual is the **`generic-transfer-key-bound`** class — promoted after round 2 (×2), not elicited by the round-3 probe (territory recorded clean), now fired here (×3 cumulative; top round-4 candidate again) |

## Reading (trend only — see taint label above)

- **Compile-pass: 0/6 → 1/6** on the exact previously-failed runs — the weakest tier-1 flip
  rate of the three rounds (round 1: 4/8; round 2: 6/8). Reported as-is. (Correction: the
  remeasure commit message and the first version of this file said "round 1: 5/8"; the
  round-1 record says 4/8.)
- **Round-3 taught-error recurrence: 0/6.** No buildlog contains any round-3 taught fragment
  (`Could not resolve the name 'event'`, `does not have the ability 'drop'`,
  `Invalid implicit copy of field`, `To use the variable mutably`) — fragment-grep plus a
  full read of every buildlog (the fragments are answer-specific literals, so grep alone
  would not establish this). The E05001/E03006 codes in the residuals are **different
  shapes** under the same codes, verified by reading the logs, not just the codes.
- **Cross-round taught-class recurrence: 1.** Several taught *codes* from earlier rounds
  appear across the six buildlogs (E01002, E03003, E03006, E05001, Sui E02009); each was
  read against its taught shape, and every appearance except one is a distinct shape under
  the same code.
  Sui E02009 (destr-3/sonnet) is a type-inference cascade of the unbound `std::mem`, not the
  taught foreign-transfer shape (analysis in the flip table). But import-2's second E03003 —
  `use std::option::{self, Option}`, lowercase `self` in a group import — **is the round-1
  taught `use-self` shape itself**, produced with the 98-claim pack (which contains that
  rule) loaded. A loaded rule ignored is recorded, not re-taught; this is the round's second
  such recurrence (the probe's was round-2's `block-statement-semicolon`).
- **Every taught fix visibly applied** in the after-answers: the import is present
  (modimp-2), the named binding is used (destr-2), the `_`-ignore is gone (destr-3/haiku),
  and `mut` is on the parameter (generic-3). The failures moved to **adjacent classes the
  beats never claimed to cover** — consistent with the experiment-4 observation that the
  residual surface is import-path / API-existence / Rust-bleed classes.
- **Four of five residual failures were already in the ledger:** `uid-reuse` (×2 → promoted),
  `std-mem-replace` (×2 → promoted), `generic-transfer-key-bound` (×3 cumulative — promoted
  after round 2, clean in the round-3 probe, fired here), and the territory-3
  `wrong-module-import` class finally showing an on-target shape — `SUI-import-path`
  (exp-4's name for it), **×3 cumulative** (exp-4 recorded it in subscription/kp61 and
  gift-card/kp86 — the very seeds of territory 3 — and this run adds the third; past the ×2
  promotion threshold → promoted). Two genuinely new classes: `rust-return-arrow` (×1,
  deferred) and `api-arity-missing-ctx` (E04016 — a framework function called with too few
  arguments, here `sui::coin::zero()` without the required `ctx`; ×1, deferred).
  **Post-measure claim freeze:** none of these are taught this round; they are the round-4
  candidate list.

The held-out effect of the round-3 beats is **unmeasured** until the next tier-2
falsification (pre-registered, fresh tasks, base-vs-kp); nothing in this file is a headline
claim.
