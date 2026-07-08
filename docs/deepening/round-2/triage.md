# Round-2 triage

Probe topline: **haiku-4-5 7/15 compile-pass (8 FAIL), sonnet-4-6 15/15 (no errors; 5 of 15 logs carry warnings)** —
the same shape as round 1. Full per-error census below uses the subsequent-error counting
convention from experiment 3 (every `error[...]` in a log is classified, not just the first).

## Failure table (every FAIL is haiku-4-5; sonnet-4-6 failed nothing)

| task | first error | all errors in log | root cause | verdict |
|---|---|---|---|---|
| modform-2 | E04007 incompatible types | E04007 ×3 | `registry.names.contains(&name)` — `sui::table` methods take the key **by value** (`K: copy + drop + store`), the model passed `&String` (Rust pass-by-reference habit); same defect at `borrow(&name)` | **beat-worthy** → `table-key-by-value` |
| modform-3 | E02004 invalid 'module' declaration | E02004 ×1 | `module fee_splitter {` — bare module name, no address qualifier. The exp-3 class, reproduced on demand by leaving naming free (4th recorded occurrence across runs) | **beat-worthy** → `module-address-form` (territory-1 target) |
| optiondrop-1 | E05001 ability constraint | E05001 ×3 | two shapes: (a) `shop.item = option::some(item)` — Option-field **overwrite** requires `drop` on the old value (×1); (b) `stock<T: store>` then `transfer::public_transfer(old_item, …)` — transferring a generic needs `T: key + store` (×2) | (a) **beat-worthy** → `option-field-fill` (territory-2 target); (b) recorded, deferred (single answer — round-3 candidate `generic-transfer-key-bound`) |
| optiondrop-2 | E03003 unbound module member | E03003 ×1, E05001 ×1 | `use std::option::{self, Option}` — the **taught** `use-self` rule ignored with the pack loaded (a rule restated is not a new rule); plus `listing.item = option::some(item)` — the same Option-overwrite shape | E03003 **recorded, not beat-worthy** (already taught; 1 ignore in 15 tasks vs 2 hits in 6 pre-deepening exp-3 tasks); E05001 counts toward `option-field-fill` |
| optiondrop-3 | E05001 ability constraint | E05001 ×1 | `capsule.gift = option::some(gift)` — Option-overwrite again (the `assert!(!is_some(...))` guard does not satisfy the compiler; the *type* still needs `drop`) | **beat-worthy** → `option-field-fill` |
| letmut-2 | E03006 unexpected name | E03006 ×1, E04003 ×4 | two Rust habits: `String::utf8(b"")` — Rust-style associated-function path (Move 2024 parses `Type::fn` as enum-variant construction; the call form is `string::utf8`) — and `result = result + sep + parts[i]` — `+` is integer-only in Move; String concatenation is `append` | **beat-worthy ×2** → `string-module-path`, `string-append` |
| letmut-3 | E01002 unexpected token | E01002 ×2 | missing `;` after a braced `if { }` (and `while { }`) used mid-sequence — Rust allows block statements without a trailing semicolon, Move's grammar requires one between sequence items | **beat-worthy** → `block-statement-semicolon` |
| coinlint-1 | Sui E02009 invalid private transfer | E02009 ×1 | `transfer::transfer(coin, ctx.sender())` on `Coin<SUI>` — a foreign (`store`) type requires `public_transfer`; the pack's `ownership-transfer` beat teaches only the **inverse** direction (public_transfer on key-only fails → use `transfer::transfer` in-module), not this mirror | **beat-worthy** → `public-transfer-foreign` |

## Warning-tier census (territories 4–5; both models, all 30 logs)

| code | hits | logs | models | verdict |
|---|---|---|---|---|
| Lint W99001 non-composable transfer to sender | 15 | 10 | **both** (haiku 6 logs, sonnet 4) | **beat-worthy** (warning-tier, GREEN + grounding — a lint warning cannot pin a RED via exit code) → `transfer-composability` |
| W04037 deprecated `vector::empty` → `vector[]` | 4 | 3 | haiku only | **beat-worthy** (warning-tier, GREEN + grounding) → `vector-literal` (territory-5 target; the recorded round-1 deferral, now measured) |
| W09009 / W09014 unused-field/function | 2 | 2 | one each | one-off untidiness, not a knowledge gap — no beat |

## Territory findings (including what did NOT reproduce)

| territory | outcome |
|---|---|
| 1 module-address-form | **confirmed** — fired exactly when naming was left free (modform-3); 2 of 3 modform tasks still compiled, so the defect is probabilistic, not universal |
| 2 Option-field `drop` | **confirmed, dominant** — the overwrite shape fired in all 3 tasks (3 hits, 3 answers); the *ignore/destructure* shape from exp-3 did **not** fire here (0 hits) — the taught fix (`option::fill` / extract-first) addresses the overwrite shape; the sibling shape is recorded in this ledger only (no pack claim covers it) |
| 3 `let mut` borrow shape (E04024) | **did not reproduce** — 0 hits in 6 letmut runs; both models now write `let mut` + `&mut` correctly (the pack's let-mut beats appear to hold). letmut-2/3 failed on *different*, previously unrecorded classes — a finding, not a wasted territory |
| 4 Coin/Balance + composability | **half-confirmed** — W99001 is pervasive (15 hits, both models: the single largest cleanliness lever); W99003 Balance-vs-Coin did **not** reproduce (0 hits — models used `Balance<SUI>` fields unprompted) |
| 5 `vector::empty` deprecation | **confirmed** — 4 hits, haiku only |

## Beat list for step 4 (9 beats)

Compile-tier (GREEN + RED + doc): `module-address-form`, `option-field-fill`,
`table-key-by-value`, `string-module-path`, `string-append`, `block-statement-semicolon`,
`public-transfer-foreign`.
Warning-tier (GREEN + doc; RED impossible — lint warnings exit 0): `transfer-composability`,
`vector-literal`.

Deferred with reasons: `generic-transfer-key-bound` (1 answer); E01003/E04010-class one-offs —
none observed this round; W09009/W09014 untidiness.
