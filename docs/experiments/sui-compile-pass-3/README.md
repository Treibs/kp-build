# sui-move falsification — experiment 3 (tier-2, deepening delta)

**Question:** did deepening round 1 (`docs/deepening/round-1/`, pack 47 → 61 claims) measurably
improve the pack on fresh held-out tasks? Round 1's own remeasure numbers are tainted by
construction (the failed tasks selected the beats); this pre-registered run is the only
legitimate source of a deepening headline.

**Pre-registration:** `tasks.md` in this directory, committed at `b5c9fe9` **before any answer
was collected** — arms, tasks, model, metrics, and the ship rule were all fixed there.
Operator sign-off for a third experiment (required by experiment 2's stopping rule): explicit
request, 2026-07-07.

## Setup (as pre-registered)

- **Arms:** `base` (task text only), `kp47` (pre-deepening pack payload, assembled from master
  `82d55df`), `kp61` (deepened pack payload, from master `8c1a2e5`). Headline comparison:
  **kp61 vs kp47**. Base is contextual only.
- **Model, all arms:** `claude-haiku-4-5`, fresh context per task per arm, headless, no tools.
- **Tasks:** 6 held-out contract-authoring tasks (escrow-swap, english-auction,
  multisig-treasury, loyalty-points, epoch-vesting, crowdfund) — none restates a pack fixture,
  a round-1 probe task, or an experiment-1/2 task.
- **Gate:** mechanical extraction → pre-declared scaffold (every declared `module X::Y` address
  name bound to `0x0`; multi-module answers gated as one package; no source edit) → plain
  `sui move build` with the pinned binary (`sui 1.74.1-8fc60f1fa966`).
- **Payload assembly:** per `tasks.md` — CONTEXT.md + a `## Pack claims (all)` section with every
  claim statement, sorted (Python `sorted()`, byte order), one bullet each. The same assembly
  code produced both pack payloads (arm-neutral). The kp47 payload carries the identical claim
  set as the round-1 probe payload (only the sort collation differs — round-1 used locale sort).

## Results

| task | base | kp47 | kp61 |
|---|---|---|---|
| escrow-swap | FAIL E03002 | FAIL E02004 | FAIL E05001 |
| english-auction | FAIL E05001 | FAIL E04024 | **PASS** WARN1 |
| multisig-treasury | PASS WARN2 | PASS WARN2 | FAIL E02004 |
| loyalty-points | FAIL Sui E01001 | PASS CLEAN | **PASS** CLEAN |
| epoch-vesting | FAIL E01003 | FAIL E02004 | **PASS** WARN1 |
| crowdfund | PASS CLEAN | FAIL E03003 | **PASS** WARN2 |
| **compile-pass (primary)** | **2/6** | **2/6** | **4/6** |
| **clean-compile (secondary)** | **1/6** | **1/6** | **1/6** |

## Verdict

**Pre-registered ship rule, branch 1: kp61 compile-pass (4/6) > kp47 compile-pass (2/6) →
deepening improves the pack.** This is the headline, measured on the primary metric with no
substitution. The secondary metric ties at 1/6 across all arms (kp61's extra passes carry
lint-tier warnings — see below), so no cleanliness claim is made for the deepening.

Scope the claim exactly: one deepening round doubled the held-out compile-pass rate for
`claude-haiku-4-5` on this task band (2/6 → 4/6, n=6). The base arm also sits at 2/6, so on
this evidence the pre-deepening pack did not lift haiku's raw compile-pass — consistent with
experiment 2's finding for sonnet (tie on primary); it is the deepening beats, taught from
measured failures, that move the primary metric.

## Failure detail (every failing row)

| task/arm | first error | root cause |
|---|---|---|
| escrow-swap/base | E03002 unbound module | `use sui::option::{self, Option}` — `option` lives in `std`, not `sui`; the import also uses lowercase `self`, the taught `use-self` corner's shape (masked here by the unbound-module error) |
| escrow-swap/kp47 | E02004 invalid 'module' declaration | `module atomic_swap {` — no address qualifier; Move 2024 requires `module <address>::name` |
| escrow-swap/kp61 | E05001 ability constraint | `escrow.item_b = option::some(item_b)` — overwriting an `Option<U>` field destroys the old value, requiring `drop` on `U` (a generic without `drop`). NOT the taught key-field-store class (same code, different rule) |
| english-auction/base | E05001 ability constraint | same Option-mutation corner: `auction.highest_bid_coin = option::some(coin)` needs `drop` on `Coin<SUI>`, which has none |
| english-auction/kp47 | E04024 invalid usage of immutable variable | reassigned a non-`mut` binding — the pack's existing let-mut rule was loaded and ignored (a restated rule, not a missing one) |
| multisig-treasury/kp61 | E02004 invalid 'module' declaration | `module treasury {` — same missing-address form |
| loyalty-points/base | Sui E01001 invalid object construction | constructed a `key` object without a fresh `object::new(ctx)` UID |
| epoch-vesting/base | E01003 invalid modifier | `struct VestingWallet has key` — missing `public`; the pack's flagship struct-visibility corner, hit by the unaided arm |
| epoch-vesting/kp47 | E02004 invalid 'module' declaration | `module linear_vesting {` — same missing-address form |
| crowdfund/kp47 | E03003 unbound module member | `use sui::coin::{self, Coin}` — lowercase `self` in a group import: **the exact corner the round-1 `use-self` beat taught.** kp61 passed this task |

**E02004 counterfactual (checked, not part of the gate):** adding the bare module name to
`[addresses]` in the scaffold's Move.toml does NOT make `module atomic_swap {` compile — E02004
persists. The failure is the model's declaration form, not a scaffold artifact. The scaffold
rule was pre-declared and applied identically to all arms. The pack (either size) does not
currently teach the module-declaration address form; E02004 appeared only in pack arms here
(kp47 ×2, kp61 ×1, base ×0) and is recorded as a round-2 beat candidate, prominently, since it
is the deepened pack's largest residual failure class in this run.

**Taught-beat error-class check (pre-registered):** of the 5 round-1 beats, exactly one taught
class appears in this run's failures — `use-self` (E03003 lowercase-`self` group import) in
**kp47**, the arm without the beat; the kp61 arm shows zero taught-class failures.
escrow-swap/kp61's E05001 shares the error *code* with the key-field-store beat but is a
different rule (Option-field mutation vs key-struct field abilities); it is counted as a new
corner, not a beat recurrence.

## Warning detail (every PASS WARN row)

| task/arm | warnings |
|---|---|
| english-auction/kp61 | W09009 unused struct field |
| multisig-treasury/base | Lint W99003 sub-optimal `Coin` field type; W04037 deprecated `vector::empty` (use `vector[]`) |
| multisig-treasury/kp47 | Lint W99003; W04037 deprecated `vector::empty` |
| epoch-vesting/kp61 | Lint W99003 sub-optimal `Coin` field type |
| crowdfund/kp61 | Lint W99001 non-composable transfer to sender (×2) |

The W04037 hits are the known `vector::empty` deprecation (a recorded round-2 deferral), not the
`exists_` rename the dynamic-field-exists beat taught. W99003/W99001 (Balance-vs-Coin field
type, transfer-to-sender composability) are untaught lint corners — with the secondary metric
tied, they are the natural targets if a cleanliness headline is ever wanted.

## Round-2 candidates surfaced by this run

1. **module-declaration address form** (E02004, 3 hits, pack arms only) — top priority.
2. **Option-field mutation requires `drop`** (E05001 shape: assign via `option::fill`/`swap` or
   extract first; 2 hits across arms).
3. **W99003 Balance-vs-Coin field idiom** and **W99001 transfer composability** (lint tier).

## Combined falsification record (experiments 1–3)

| | exp 1 (sonnet, representative) | exp 2 (sonnet, harder, pre-reg dual metric) | exp 3 (haiku, held-out, deepening delta) |
|---|---|---|---|
| compile-pass | base 5/5 = kp 5/5 (ceiling) | base 4/5 = kp 4/5 (tie) | base 2/6, kp47 2/6, **kp61 4/6 → ships rule branch 1** |
| clean-compile | post-hoc only | **kp 3/5 > base 2/5 → shipped rule branch 2** | tie 1/6 all arms |

Honesty notes: n=6 per arm is small — the headline is the pre-registered comparison clearing its
pre-registered rule, not a general benchmark claim. All numbers above are pinned to the pack
size and model they measured. Committed buildlogs are ANSI-stripped and home-directory-redacted;
the scaffold `build/` outputs and `Move.lock` files are gitignored, so the committed artifacts
are the answers, extracted sources, Move.toml scaffolds, buildlogs, and verdicts.
