# Experiment 5 — held-out falsification of deepening round 3 (sui-move)

**Result up front: no round-3 headline.** The primary metric tied (kp98 3/6 = kp86 3/6), so
round 3's 12 added claims did not raise held-out compile-pass; and on the secondary metric
**kp98 regressed: 1/6 clean-compile vs kp86's 3/6.** All three warnings that cost kp98 its
clean passes are `Lint W99001` (non-composable transfer to sender) — the exact class the
round-2 `transfer-composability` beat teaches, loaded in the kp98 payload at the time. The
pre-registered ship rule lands on branch 3; the secondary regression is reported here as
prominently as a win would have been. One result did move in the pack's favor on this draw:
both pack arms beat base on the primary (3/6 vs 2/6), and the flipped task
(insurance-pool) failed in base on the original taught `struct-visibility` class — the
pack's oldest beat, still doing its job.

## Setup

- Pre-registration: [`tasks.md`](tasks.md), committed at `137b267` **before any answer was
  collected** — arms, tasks (held-out audit run before drafting froze; four candidates dropped
  by it, disclosed there), metrics, the three-branch ship rule, and the pre-registered
  vocabulary-induction analysis method.
- Arms: **base** (task + instruction only), **kp86** (pack payload as of master `86989a1`,
  86 claims — pre-round-3, byte-identical to experiment 4's kp86 arm), **kp98** (pack payload
  as of master `17f3210`, 98 claims — post-round-3). Payloads assembled by the arm-neutral rule
  in tasks.md (`CONTEXT.md` + all claim statements, sorted).
- Model: `claude-haiku-4-5`, fresh context per task per arm, headless, no tools.
- **Protocol fix carried from experiment 4's disclosure:** the headless CLI ran from a neutral
  scratch working directory for all arms, so no answer could inherit repo-name vocabulary from
  the process environment.
- Gate: mechanical first-fenced-block extraction, arm-neutral scaffold (`Move.toml` binding the
  answer's own module address names to `0x0`), plain `sui move build` on the pinned
  `sui 1.74.1-8fc60f1fa966`. Committed buildlogs are ANSI-stripped and home-directory-redacted.
- Layout: `answers/<task>/<arm>.answer|-src.move|-pkg/|.buildlog|.result`; summary in
  [`answers/results.txt`](answers/results.txt).
- The assembled payloads themselves are not committed; they are mechanically reproducible from
  the assembly rule in tasks.md (the pinned commits + `sorted()` claim statements).
- **Erratum in the frozen pre-registration** (tasks.md is not edited post hoc): its context
  sentence "sonnet-4-6 probed 13/15 with the pack loaded in round 3; its two valid failures
  were one task" is wrong — the round-3 probe record (`docs/deepening/round-3/triage.md`) has
  sonnet 13/15 with one of the two failures VOID (import-3, the reserved-word task defect), so
  sonnet had ONE valid probe failure (destr-3). Context-only; no arm, task, metric, or ship-rule
  text is affected.

## Results

| task | base | kp86 | kp98 |
|---|---|---|---|
| ballot-box | PASS CLEAN | PASS CLEAN | PASS CLEAN |
| insurance-pool | FAIL E01003 | **PASS CLEAN** | **PASS WARN2** |
| hash-riddle | FAIL E01003 | FAIL E03003 | FAIL E04007 |
| allowance-vault | FAIL E05001 | FAIL E01002 | FAIL E03006 |
| milestone-contract | FAIL E01003 | FAIL E03003 | FAIL E04023 |
| oracle-feed | PASS CLEAN | PASS CLEAN | PASS WARN1 |
| **primary — compile-pass** | **2/6** | **3/6** | **3/6** |
| **secondary — clean-compile** | **2/6** | **3/6** | **1/6** |

## Verdict (pre-registered ship rule)

- Branch 1 (kp98 > kp86 primary): **no** — tie.
- Branch 2 (primary tie AND kp98 > kp86 secondary): **no** — kp98 is *below* kp86 on the
  secondary (1/6 vs 3/6).
- **Branch 3: no round-3 headline on this evidence; recorded as-is.** kp98 is not below kp86
  on the primary, so this is not a primary regression under the rule — but **the cleanliness
  regression is real and attributable to a specific ignored rule:** kp98's two non-clean passes
  carry three `Lint W99001` hits (`transfer::transfer(cap, ctx.sender())` in insurance-pool
  plus `transfer::public_transfer(withdrawal_coin, ctx.sender())` there, and
  `transfer::public_transfer(cap, ...sender(ctx))` in oracle-feed), the class the round-2
  `transfer-composability` grounding beat targets. The rule was in the kp98 payload for every one of those answers.
  kp86's three passes were all clean, and W99001 appeared nowhere else in any passing log.

Context notes, neither of which changes the verdict:

1. **Unlike experiment 4's draw, this one left headroom, and the pack used some of it.** Base
   solved 2/6 (exp-4's base: 5/6 — task draws are not comparable across experiments). Both
   pack arms took the same +1 over base, on the task whose base failure was the original taught
   `struct-visibility` class.
2. **The round-3 delta had nothing to grip on this draw.** None of kp86's three failures
   root-cause on a class round 3 taught (they fall on classes taught in rounds 1–2 but
   ignored, plus untaught SUI-import / Rust-bleed shapes — detail below). So round 3's beats
   could not have flipped these tasks, and kp98 indeed flipped none of them: on each, its
   answer avoided kp86's failure class and found a different untaught one.

## Failure detail (every failing row; all `error[` lines classified)

| task/arm | errors in log | root cause | class |
|---|---|---|---|
| insurance-pool/base | E01003 ×7 | `struct InsurancePool has key { ... }` etc. — seven struct declarations without `public` ("Visibility annotations are required on struct declarations from the Move 2024 edition onwards") | **original taught `struct-visibility` class** — fired only in the no-pack arm; both pack arms passed this task |
| hash-riddle/base | E01003 ×1, E03003 ×1 | two independent root causes: a `struct` without `public`; and `hash::sha3_256` called in `sui::hash` ("Unbound function 'sha3_256' in module 'sui::hash'" — `sha3_256` lives in `std::hash`) | **original taught `struct-visibility` class** + wrong-module hash API (untaught) |
| allowance-vault/base | E05001 ×6 | `public struct Allowance has store` stored via `dynamic_object_field` — `remove` requires `key` (+`store`), and `let _: Allowance = dynamic_object_field::remove(...)` additionally needs `drop` to discard | dof-value-ability (untaught) — the only failure in the experiment rooted on a pre-registered vocabulary surface, and it is in the **base** arm |
| milestone-contract/base | E01003 ×1, E05001 ×2, E06001 ×2 | a `struct` without `public`; and `transfer::public_transfer(contract.balance, ...)` without unpacking the struct — "Invalid implicit copy of field 'balance' without the 'copy' ability" (E05001), with the un-consumed `contract` then flagged E06001; one design defect, two symptom codes | **original taught `struct-visibility` class** + **round-3 taught `implicit-field-copy` class** (exact message template — the fixture pins "Invalid implicit copy of field 'gem'…", the log reads "…field 'balance'…"; identical modulo the field identifier) — both fired only in the no-pack arm; both pack arms avoided them |
| hash-riddle/kp86 | E03003 ×1, E03006 ×4 | `use sui::coin::{Coin, SUI, Self}` — `SUI` is not in `sui::coin` (it is `sui::sui::SUI`); all four E03006 are downstream uses of the unbound `SUI` | **SUI-import-path** (untaught; round-4 candidate, wrong-module shape) |
| allowance-vault/kp86 | E01002 ×2, E05001 ×2, E06001 ×1 | **three independent root causes:** (1) `fun create_vault(...) -> OwnerCap` — Rust return arrow (E01002 "Unexpected '->'"; the E06001 on the unconsumed `coin` parameter is parse-recovery fallout — "Expected '{'" dropped the body that consumes it at `coin::into_balance(coin)`); (2) `vault.allowance = option::some(...)` / `= option::none()` on `Option<Allowance>` where `Allowance` lacks `drop` — E05001 "Invalid mutation. Mutation requires the 'drop' ability as the old value is destroyed"; (3) `if (...) { ... }` followed by a statement with no `;` — E01002 "Unexpected 'assert' / Expected ';'" | rust-return-arrow (untaught; round-3 deferral, ×2 cumulative) + **round-2 taught `option-field-fill` class (exact fragment)** + **round-2 taught `block-statement-semicolon` class** — two loaded rules ignored in one answer |
| milestone-contract/kp86 | E03003 ×2, E03006 ×1 | `use sui::coin::{self, Coin}` and `use sui::object::{self, UID}` — lowercase `self` in group imports; the E03006 is a downstream `coin::split` | **round-1 taught `use-self` class** — a loaded rule ignored (the second such event for this class; round-3's remeasure recorded one) |
| hash-riddle/kp98 | E04007 ×2 | `hash::sha2_256(&answer)` — `std::hash::sha2_256` takes `data: vector<u8>` by value; the answer passed `&vector<u8>` (both call sites) | api-byref-arg — Rust-style by-reference argument passing; sibling of the round-3-deferred `api-arity-missing-ctx` (wrong-signature family). **The loaded round-2 `table-key-by-value` claims teach this exact habit** ("passing a table key by reference (`table.contains(&key)`, the Rust habit)" — same E04007, same "Invalid call of … Invalid argument for parameter" template) but pin it to `sui::table` keys specifically; at the fixture-rule scope the recurrence check uses, this is a *new API* for a *loaded rule shape* — recorded as loaded-rule-adjacent, not recurrence. Note the module and function are *right* this time (base's answer had used `sui::hash::sha3_256`) |
| allowance-vault/kp98 | E03006 ×4, E05001 ×2 | two independent root causes: (1) `SUI` referenced (`Balance<SUI>`, `Coin<SUI>`) but never imported — no `use sui::sui::SUI` anywhere (all four E03006); (2) `let _ = option::extract(&mut vault.allowance)` — "Cannot ignore values without the 'drop' ability" (both E05001) | **SUI-import family, absent-import shape** — no loaded claim teaches `use sui::sui::SUI` (the wrong-module shape is recorded in exp-4 and hash-riddle/kp86 above); the E03006 message template ("Could not resolve the name 'SUI'") matches the round-3 `missing-module-import` fixture's ("…the name 'event'") modulo identifier, but that beat pins module-alias *calls* (`use sui::module` before `module::fn`), a different rule with a different fix — loaded-rule-adjacent at template scope, not recurrence + let-discard — the compile-tier fixture scope is untaught (round-3 `destructure-ignore` pins the field-level `field: _` shape; this is the value-level `let _ =` sibling, exp-3's "drop on discard" lineage), **but the loaded round-3 `destructure-ignore-doc` claim states the general rule verbatim** ("The `drop` ability gates every way of ignoring a value — including leaving a local or parameter unused"), so this too is a loaded rule not applied |
| milestone-contract/kp98 | E04023 ×6 | `milestones.len()` and `milestones.get(i)` — `std::vector` has no `len`/`get` (Move 2024 methods are `.length()` / `.borrow(i)`); six call sites, one habit | rust-vector-method (new) — Rust `Vec` API bleed; family sibling of rust-return-arrow and the taught block-statement-semicolon |

**Taught-beat recurrence (pre-registered check, original pack + rounds 1, 2, 3):** the
recurrence standard, stated explicitly: a hit counts as recurrence when the answer's defect is
the *rule* a fixture pins (same defect shape, same fix), with the error message matching the
fixture fragment up to answer-specific identifiers; a defect whose message template matches
but whose pinned rule and fix differ is recorded as *loaded-rule-adjacent*, not recurrence.
By that standard the arms split sharply. In **base**, taught classes did the failing: original
`struct-visibility` in 3 of 4 failing rows and round-3 `implicit-field-copy` (message template
modulo the field name) in one — and both pack arms avoided every one of those hits. In
**kp86**, three taught classes recurred *with their rules loaded*: round-1 `use-self`, round-2
`option-field-fill` (byte-exact fragment), and round-2 `block-statement-semicolon` — five
error sites across two tasks, all loaded-rule-ignored events. In **kp98**, zero error-tier
taught classes recurred at that standard — but the qualifier cuts against kp98, not for it:
two of its three failures sit directly adjacent to loaded rules (the E04007 by-ref habit the
round-2 `table-key-by-value` claims teach for table keys, applied here to `std::hash`; the
`let _ =` discard the loaded `destructure-ignore-doc` claim's general wording covers
verbatim), and at the warning tier it ignored the loaded round-2 `transfer-composability`
rule three times (the entire secondary regression). Net: the pack's beats demonstrably encode
real failure classes (base keeps hitting them), but on this draw the binding constraint was
rule *salience*, not rule *coverage* — 8 of the pack arms' recorded defect events (5 error
sites + 3 warnings) were rules literally in the loaded payload, and kp98's loaded-rule-adjacent
events (E04007 ×2, E05001 ×2) push the same diagnosis further.

## Pre-registered vocabulary-induction analysis (observational, no ship-rule weight)

Experiment 4 recorded a hypothesis (fit 3 of its 6 failing pack-arm rows, post hoc): the pack's
idiom vocabulary prompts more ambitious designs whose extra API surface creates failure
opportunities base answers never encounter. This experiment pre-registered the test method in
tasks.md before any answer existed. Applying it:

**A failing pack-arm row supports the hypothesis iff its root cause sits on a pre-registered
surface ({table, event, balance, clock, dynamic fields, package/display}) that the base answer
for the same task avoided while base passed. Result: 0 of 6 failing pack-arm rows fit.** Every
pack-arm failure occurred on a task base *also* failed (so no row could fit regardless of
surface), and independently, none of the nine pack-arm root causes above sits on a
pre-registered surface — they are import paths, Rust-syntax bleed, ability/discard shapes, and
a hash-function signature. The base-failure census cuts the same way: the only
surface-rooted failure in all 18 rows is allowance-vault/**base** (dynamic object fields,
unprompted).

The usage half of the mechanism is still visible in the census: pack arms referenced
pre-registered surfaces base did not on hash-riddle (base none; kp86 event+balance; kp98
event+clock), allowance-vault (both pack arms clock; base none — base reached for dynamic
object fields instead), and milestone-contract (base and kp86 none; kp98 event) — but none of that extra
surface was where the failures landed, and it did not cost length (mean lines: base 97, kp86
102, kp98 95). Per the pre-registered method, this draw **does not support** the
vocabulary-induction hypothesis; experiment 4's 3-of-6 post-hoc fit did not replicate under
the committed rule.

Full census (line count + pre-registered surfaces referenced, per task × arm):

| task | base | kp86 | kp98 |
|---|---|---|---|
| allowance-vault | 105 — balance,dynfield | 100 — balance,clock | 110 — balance,clock |
| ballot-box | 109 — table | 103 — table | 91 — table |
| hash-riddle | 80 — (none) | 128 — event,balance | 105 — event,clock |
| insurance-pool | 158 — event,balance | 124 — event,balance | 102 — balance |
| milestone-contract | 71 — (none) | 93 — (none) | 114 — event |
| oracle-feed | 61 — event | 64 — event | 46 — event |

## Warning detail

- `Lint W99001` (non-composable transfer to sender): **3 hits, all in kp98 passing logs**
  (insurance-pool ×2, oracle-feed ×1) — the only warnings in any passing log this experiment,
  and the whole secondary regression. The round-2 `transfer-composability` beat teaches exactly
  this; the rule was loaded and ignored. In experiment 4 this lint was at 0 hits in all 18 logs.
- `Lint W99003` (Coin field where Balance fits): 5 hits, all in failing logs (hash-riddle
  base/kp98, milestone-contract all three arms' failing rows) — no effect on the secondary.
- `W04037` ×2 (allowance-vault/base), `W09002` unused-variable ×3 — failing logs only. The
  W04037 hits are the `exists_` → `exists` deprecation, the class the round-1
  `dynamic-field-exists` grounding beat teaches, firing in the *no-pack* arm (both pack arms
  avoided dynamic fields on this task entirely; the beat pins `dynamic_field`, this answer
  used `dynamic_object_field`, so fixture-rule-scope credit is arguable — recorded, not
  claimed).

## Round-4 candidates recorded by this experiment

1. **SUI-import family** — now the top candidate, two shapes: wrong-module
   (`use sui::coin::{..., SUI}`; hash-riddle/kp86 here, 2 tasks in exp-4, and one round-3
   remeasure task — import-2 — whose one unbound `SUI` cascaded to ×3 error sites) and
   absent-import (`SUI` used, never imported; allowance-vault/kp98 here). One
   beat showing `use sui::sui::SUI` covers both.
2. **Rust-bleed family** — rust-return-arrow (allowance-vault/kp86; ×2 cumulative with the
   round-3 deferral) and NEW **rust-vector-method** (`.len()`/`.get()` on `vector`;
   milestone-contract/kp98, ×6 sites). The already-taught `block-statement-semicolon` is the
   same family — its recurrence is a salience problem, not a coverage gap.
3. **hash-functions corner** — two different failures on one API in one task: base called
   `sha3_256` in the wrong module (`sui::hash`), kp98 passed `&vector<u8>` by reference
   (**api-byref-arg**, new). A hash beat pins module path + by-value signature at once.
4. **let-discard** — `let _ = <non-drop value>` (allowance-vault/kp98 ×2; allowance-vault/base
   also hit it ×2 inside its E05001 pile-up); the value-level sibling of the taught
   `destructure-ignore`.
5. **dof-value-ability** — `dynamic_object_field` values need `key`+`store`
   (allowance-vault/base ×6 sites); base-arm only, lower priority.
6. Carried from the round-3 ledger, did not fire here: `uid-reuse` (×2), `std-mem-replace`
   (×2), `generic-transfer-key-bound` (×3).
7. **Not a beat: the loaded-rule-ignored phenomenon.** Eight defect events across the pack
   arms were rules present in the loaded payload (use-self, option-field-fill,
   block-statement-semicolon, transfer-composability ×3). Two consecutive experiments now
   show pack growth failing to convert to held-out gains; the recorded alternative to a
   round 4 is a payload-salience/slimming experiment on the existing 98 claims.

## Combined record (experiments 1–5)

| | exp 1 (sonnet, representative) | exp 2 (sonnet, harder, pre-reg) | exp 3 (haiku, round-1 delta, pre-reg) | exp 4 (haiku, round-2 delta, pre-reg) | exp 5 (haiku, round-3 delta, pre-reg) |
|---|---|---|---|---|---|
| compile-pass | base 5/5 = kp 5/5 (ceiling) | base 4/5 = kp 4/5 (tie) | base 2/6, kp47 2/6, **kp61 4/6 → shipped branch 1** | **base 5/6**, kp61 3/6, kp86 3/6 → branch 3, base beat both pack arms | base 2/6, **kp86 3/6 = kp98 3/6** → branch 3; pack arms beat base |
| clean-compile | post-hoc only | **kp 3/5 > base 2/5 → shipped branch 2** | 1/6 all arms | base 3/6, kp61 2/6 = kp86 2/6 | base 2/6, kp86 3/6, **kp98 1/6 — regression** |

The honest cumulative reading: the pack's held-out wins remain exp 2's cleanliness claim
(sonnet) and exp 3's compile-pass doubling (haiku, round-1 delta). Since then, two rounds of
growth (61 → 86 → 98 claims) have produced two consecutive no-headline experiments: held-out
compile-pass for the pack arms has sat at 3/6 across two consecutive task draws (four
pack-arm measurements over three pack versions: kp61, kp86 twice, kp98), and the newest
round cost cleanliness through ignored loaded warnings. The failure mass has moved twice —
exp 4 said it was import-path and API-existence slips; exp 5 says it is (a) rules the payload
already contains being ignored at answer time, and (b) the untaught SUI-import and Rust-bleed
families. That leaves two forks for the next unit of work, both recorded above: a *small*
round 4 (SUI-import + Rust-bleed + hash corner — beats aimed at classes with multi-experiment
recurrence), or a payload-salience experiment that stops growing the pack and tests whether
fewer, better-surfaced claims convert to more rules applied.
