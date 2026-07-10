# Sui Move fixture beat log

Every claim below was established by running the real pinned compiler — not from memory.

- **Binary:** `sui 1.74.1-8fc60f1fa966` (`$KP_BUILD_SUI_BIN`, the Task-0 pinned binary)
- **Date:** 2026-07-06
- **Build command:** `sui move build` (plain — matches `sui_runner.py` and the acceptance gate)
- **Framework:** implicit dependency, pinned by the toolchain to MystenLabs/sui git rev
  `b124567746b3a78a7e294ac2de265f693401ec9d` (recorded in each committed `Move.lock`)

Classification rule: RED errors → paired fixture ships with `expected_error.txt` (fragment
taken from the *observed* output). RED compiles or only warns → red dropped, beat is
grounding-only (green + doc-grounding claim).

## Triage table

| beat | red form tried | observed (exit + key output) | classification | fragment (expected_error.txt) |
|---|---|---|---|---|
| struct-visibility | bare `struct` (no visibility) | exit 1, `error[E01003]: invalid modifier` + note | RED/GREEN pair | `Visibility annotations are required on struct declarations` |
| method-syntax | legacy `friend method_syntax_red::admin;` declaration | exit 1, `error[E13002]: feature is deprecated in specified edition` (fires before the secondary `unbound module` error) | RED/GREEN pair | `'friend's are deprecated. Remove and replace 'public(friend)' with 'public(package)'` |
| implicit-imports | legacy `use sui::object::{Self, UID}; use sui::transfer; use sui::tx_context::TxContext;` block | exit 0, **no warning at all** (surprise: expected a duplicate-alias warning; 1.74.1 accepts the legacy block silently) | grounding-only (green kept) | — |
| abilities | `key` struct without `id: UID` first field | exit 1, `error[Sui E02007]: invalid object declaration` (plus secondary `Sui E01001` invalid object construction) | RED/GREEN pair | `Structs with the 'key' ability must have 'id: sui::object::UID' as their first field` |
| macros-2024 | pre-2024 rebinding of a local declared without `mut` | exit 1, `error[E04024]: invalid usage of immutable variable` (x2, one per variable) | RED/GREEN pair | `Invalid assignment of immutable variable` |
| object-new | fabricated `object::uid_from_bytes(b"1234")` | exit 1, `error[E03003]: unbound module member` | RED/GREEN pair | `Unbound function 'uid_from_bytes' in module 'sui::object'` |
| ownership-transfer | `transfer::public_transfer` on a `key`-only struct (no `store`) | exit 1, `error[E05001]: ability constraint not satisfied` | RED/GREEN pair | `The type 'ownership_transfer_red::item::Item' does not have the ability 'store'` |
| entry-vs-public | `public entry fun` (red candidate built in /tmp scratch, not committed) | exit 0, `warning[Lint W99010]: unnecessary 'entry' on a 'public' function` — warning only, as expected; the committed green is plain `public fun` | grounding-only (green kept) | — |
| otw-init | `init(value: u64, ctx: &mut TxContext)` — first param not a one-time witness | exit 1, `error[Sui E02003]: invalid 'init' function` (init signature IS checked at build time) | RED/GREEN pair | `Invalid parameter 'value' of type 'u64'. Expected a one-time witness type` |
| capability | auth via `assert!(ctx.sender() == @0xCAFE)` hardcoded sender check | exit 0, no warnings — compiles clean, as expected (design rule, not a compiler rule) | grounding-only (green kept) | — |
| coin-currency | fabricated `coin::mint_new(witness, 9, b"MYC", ctx)` | exit 1, `error[E03003]: unbound module member` | RED/GREEN pair | `Unbound function 'mint_new' in module 'sui::coin'` |
| dynamic-fields | fabricated `object::add_field(&mut container.id, name, value)` | exit 1, `error[E03003]: unbound module member` | RED/GREEN pair | `Unbound function 'add_field' in module 'sui::object'` |
| events | event struct missing `copy` (kept `drop` so the error is attributable to one ability) | exit 1, `error[E05001]: ability constraint not satisfied` against `event::emit<T: copy + drop>` | RED/GREEN pair | `The type 'events_red::notify::ValueSet' does not have the ability 'copy'` |
| clock | fabricated `tx_context::now_ms(ctx)` | exit 1, `error[E03003]: unbound module member` | RED/GREEN pair | `Unbound function 'now_ms' in module 'sui::tx_context'` |
| test-scenario | `take_shared` without `return_shared` in a `#[test]` | **exit 0 under plain `sui move build`** — surprise: plain build does NOT compile `#[test]` code on 1.74.1 (verified by planting a type error in a test fn: plain build exit 0, `--test` build exit 1). Under `sui move build --test` the red DOES fail: exit 1, `error[E06001]: unused value without 'drop'`. The pack's runner and acceptance gate use plain build → red cannot ship. | grounding-only (green kept; red dropped) | — |
| test-only | non-test `public fun` calling a `#[test_only]` fn | exit 1, `error[E03005]: unbound unscoped name` — surprise: the diagnostic is a plain unbound-name error (test_only members are *filtered out* of non-test builds), not a dedicated test_only message | RED/GREEN pair | `Unbound function 'create_for_testing' in current scope` |

**Totals:** 16 green fixtures, 12 red fixtures (4 beats grounding-only: implicit-imports,
entry-vs-public, capability, test-scenario).

Grounding-only red candidates were built in a scratch dir (`/tmp/sui-triage/candidates/`,
not committed) to *prove* they compile — classification is observed, not assumed.

## Surprises vs. expectations

1. **Plain `sui move build` skips `#[test]`/`#[test_only]` code.** The task expectation
   ("`sui move build` compiles test code") is false on 1.74.1. Proven by planting
   `counter.value() == true` inside a `#[test]` fn: plain build exit 0, `--test` exit 1
   (E04007-class type error). Consequences:
   - test-scenario red reclassified grounding-only (see table).
   - Both test-beat greens were *additionally* verified with `sui move build --test`
     (exit 0 for `test-scenario-green` and `test-only-green`), so the committed test code
     is known to typecheck even though the plain gate doesn't exercise it.
2. **`coin::create_currency` is deprecated on 1.74.1** — builds with
   `warning[W04037]: deprecated usage: ... Use 'coin_registry::new_currency_with_otw' instead`
   (exit 0, so green passes the gate). Kept as the green: it is still the documented,
   universally available idiom, and the beat's mechanical claim contrasts it with the
   fabricated `coin::mint_new`. The research.json claim text (Task 5) should mention the
   deprecation so the pack doesn't overclaim "current best practice".
3. **Legacy import block is completely silent** (implicit-imports beat): expected at least
   a duplicate-alias warning; got none.
4. **Compiler typo, for the record:** the E05001 output spells "constraint not satisifed".
   Fragments deliberately use the type-sentence line instead.

## Offline reproducibility

- `unshare -rn true` fails on this host (`write failed /proc/self/uid_map: Operation not
  permitted`; no passwordless sudo), so a network namespace test was not possible.
- Substitute test 1 — syscall trace: cold build (fixture `build/` deleted) of
  `struct-visibility-green` under `strace -f -e trace=connect,sendto,recvfrom`. The only
  outbound connection is to `fullnode.testnet.sui.io` (443) — the CLI's tree-shaking RPC
  (see `--no-tree-shaking` help). No git/github fetch: the framework dependency is served
  from the warm local cache `~/.move/git/...MystenLabs_sui...b124567746b3a78a7e294ac2de265f693401ec9d/`.
- Substitute test 2 — dead proxy: cold build with
  `https_proxy=http_proxy=HTTPS_PROXY=HTTP_PROXY=http://127.0.0.1:1` → **exit 0**. The RPC
  attempt is best-effort; the build succeeds without reachable network.
- **Verdict: offline reproducible given the warm `~/.move` framework cache** (which the
  pinned binary populates keyed to its own rev). A truly cold machine (no `~/.move`) would
  need one initial fetch of the framework packages.
- **Pinning decision:** `[dependencies]` left empty on purpose. The implicit framework dep
  is pinned by the toolchain to the rev matching the binary (recorded in `Move.lock`);
  adding an explicit `Sui = { git = ..., rev = ... }` would *add* a git fetch path, making
  offline behavior worse, not better.

## Move.lock decision

`Move.lock` files are committed for all 16 green fixtures: the file header itself says
"This file should be checked in", each is ~1KB, and they pin the exact framework source
(git rev `b1245677...`) per environment — they ARE the reproducibility pins. Red fixtures
have no `Move.lock`: the CLI only writes it on successful builds, and red builds fail by
design. `build/` output dirs are gitignored (`examples/sui-move-fixtures/**/build/`).

## Revision beat — receiving (proven 2026-07-07)

Queued from the pack-revision pass (the transfer-to-object pattern was a probe weakness left
uncovered at ship time). Same pinned binary (`sui 1.74.1-8fc60f1fa966`), same plain-build gate.

| beat | red form tried | observed (exit + key output) | classification | fragment (expected_error.txt) |
|---|---|---|---|---|
| receiving | `transfer::receive` on a type defined in a *different* module (internal rule) | exit 1, `error[Sui E02009]: invalid private transfer call` — "restricted to being called in the object's module" | RED/GREEN pair | `The function 'sui::transfer::receive' is restricted to being called in the object's module` |

Triage notes (scratch candidates in `/tmp/sui-triage2/`, not committed):
- **red-a candidate** (`public_receive` on a `key`-only type) also fails — `error[E05001]`,
  `'store' constraint not satisifed` — but that duplicates the ownership-transfer red's error
  class. Dropped in favour of the receive-specific internal-rule error.
- **red-b (shipped)** is a new error class for the pack (Sui E02009), specific to the private
  transfer rules; the green's `public_receive` (`T: key + store`) is the cross-module escape,
  mirroring `transfer` vs `public_transfer`.
- green builds clean; `Move.lock` pins the same framework rev `b124567746b3a78a7e294ac2de265f693401ec9d`.

**Totals:** 17 green fixtures, 13 red fixtures (4 beats grounding-only, unchanged).

## Deepening round 1 — 5 beats (proven 2026-07-07)

Source: the first /kp-deepen round (`docs/deepening/round-1/`) — probe of 5 unprobed
territories, 15 tasks × 2 models with the current pack loaded, gated by the same pinned
binary (`sui 1.74.1-8fc60f1fa966`, plain build). Every beat below traces to an observed
probe failure (compile-tier) or a counted warning family (warning-tier); triage table in
`docs/deepening/round-1/triage.md`.

| beat | red form tried | observed (exit + key output) | classification | fragment (expected_error.txt) |
|---|---|---|---|---|
| use-self | Rust-style `use sui::coin::{self, Coin};` | exit 1, `error[E03003]: unbound module member` at the `use` line | RED/GREEN pair | `Invalid 'use'. Unbound member 'self' in module 'sui::coin'` |
| type-name | `vector<std::string::String>` field receiving `type_name::with_defining_ids<T>()` | exit 1, `error[E04007]: incompatible types` | RED/GREEN pair | `Given: 'std::type_name::TypeName'` |
| witness-naming | plain witness named `MINTER` (upper-case of module `minter`), constructed manually | exit 1, `error[Sui E02005]: invalid one-time witness usage` | RED/GREEN pair | `One-time witness types cannot be created manually` |
| key-field-store | `key` struct with `posts: vector<Post>` where `Post` has no abilities | exit 1, `error[E05001]: ability constraint not satisfied` (field-type variant) | RED/GREEN pair | `The struct was declared with the ability 'key' so all fields require the ability 'store'` |
| dynamic-field-exists | n/a — `exists_` still *compiles* (warns `W04037` deprecated: "Renamed to `exists`"), so a red cannot fail the plain-build gate | green (`dynamic_field::exists`) exit 0, zero warnings | grounding-only (green + doc) | — |

Notes:
- New error classes for the pack: `Sui E02005` and `E04007`; plus new message shapes under
  E03003 (the "Invalid 'use'" variant) and E05001 (the field-type variant).
- The type-name green also folds in the 1.74.1 deprecation of `std::type_name::get`
  ("Renamed to `with_defining_ids`"), observed 6× across probe answers.
- Triaged-out candidates this round (reasons in the round ledger): the generic
  `unlock<T: store>` + `public_transfer` failure (rule already loaded —
  ownership-transfer-green states `key + store` verbatim); `std::vector::empty`
  deprecation (deferred, small edition-syntax corner); W99001/W99002 composability
  lints (design-tier, no beat shape yet).
- Greens' `Move.lock` pin the same framework rev `b124567746b3a78a7e294ac2de265f693401ec9d`.

**Totals:** 22 green fixtures, 17 red fixtures (5 beats grounding-only: implicit-imports,
entry-vs-public, capability, test-scenario, dynamic-field-exists).

## Deepening round 2 — 9 beats (proven 2026-07-07)

Source: the second /kp-deepen round (`docs/deepening/round-2/`) — gap-seeded from the
experiment-3 recorded candidates plus round-1 deferrals; 15 tasks × 2 models with the
61-claim pack loaded, gated by the same pinned binary (`sui 1.74.1-8fc60f1fa966`, plain
build). Triage table in `docs/deepening/round-2/triage.md`. Every compile-tier beat traces
to an observed haiku-4-5 probe failure; the two warning-tier beats trace to the probe's
warning census (W99001: 15 hits across 10 of 30 logs, both models; W04037: 4 hits, haiku only).

| beat | red form tried | observed (exit + key output) | classification | fragment (expected_error.txt) |
|---|---|---|---|---|
| module-address-form | bare `module fee_splitter {` (no address qualifier) | exit 1, `error[E02004]: invalid 'module' declaration` | RED/GREEN pair | `The module does not have a specified address` |
| option-field-fill | `slot.item = option::some(item)` where `Item` has `store` but no `drop` | exit 1, `error[E05001]: ability constraint not satisfied` — the *mutation* variant: "Mutation requires the 'drop' ability as the old value is destroyed" | RED/GREEN pair | `Invalid mutation. Mutation requires the 'drop' ability as the old value is destroyed` |
| table-key-by-value | `names.contains(&name)` — key passed by reference | exit 1, `error[E04007]: incompatible types` (Given `&std::string::String`, expected `std::string::String`) | RED/GREEN pair | `Invalid call of 'sui::table::contains'. Invalid argument for parameter 'k'` |
| string-module-path | Rust-style `String::utf8(b"hello")` associated path | exit 1, `error[E03006]: unexpected name in this position` (parsed as enum-variant construction) | RED/GREEN pair | `Invalid construction. Expected an enum` |
| string-append | `a + b` on `std::string::String` values | exit 1, `error[E04003]: built-in operation not supported` | RED/GREEN pair | `Invalid argument to '+'` |
| block-statement-semicolon | braced `if (x > cap) { x = cap }` mid-sequence with no trailing `;` | exit 1, `error[E01002]: unexpected token` at the *next* statement | RED/GREEN pair | `Expected ';'` |
| public-transfer-foreign | `transfer::transfer(coin, recipient)` on `Coin<SUI>` in a foreign module | exit 1, `error[Sui E02009]: invalid private transfer call` | RED/GREEN pair | `The function 'sui::transfer::transfer' is restricted to being called in the object's module, 'sui::coin'` |
| transfer-composability | n/a — `public_transfer(.., ctx.sender())` only *warns* (`warning[Lint W99001]: non-composable transfer to sender`, exit 0), so a red cannot fail the plain-build gate | green (public fun returns the object) exit 0, zero warnings | grounding-only (green + doc) | — |
| vector-literal | n/a — `std::vector::empty<u64>()` only *warns* (`warning[W04037]: deprecated usage ... Use `vector[]` literal instead`, exit 0) | green (`vector[]` + `vector[a, b]` literals) exit 0, zero warnings | grounding-only (green + doc) | — |

Notes:
- New error classes for the pack: `E02004`, `E03006`, `E04003`, `E01002`; plus new message
  shapes under E05001 (the mutation variant) and E04007 (the by-reference table-key variant).
  `Sui E02009` recurs from the receiving beat, but as the *inverse rule direction*: the pack's
  ownership-transfer beat taught "public_transfer needs store"; this beat teaches "foreign
  store types need public_transfer, not transfer".
- Both warning-tier warn-forms were proven in a scratch dir (`/tmp/kp-r2/warn-candidates/`,
  not committed) — classification is observed, not assumed, same rule as round 1.
- option-field-fill fixtures gained a `value()` accessor to silence an unrelated `W09009`
  unused-field warning so the greens stay zero-warning.
- Corpus extended (same pinned commits as the original vendoring — move-book `8ce4dcb9`,
  sui `d9f4797d`) with: `book/move-basics/module.md`, `reference/variables.md` (expression
  blocks), `reference/primitive-types/vector.md` (literals), `std/option.md` (fill/swap),
  `std/string.md` (utf8/append), `std/vector.md` (empty).
- Greens' `Move.lock` pin the same framework rev `b124567746b3a78a7e294ac2de265f693401ec9d`.

**Totals:** 31 green fixtures, 24 red fixtures (7 beats grounding-only: implicit-imports,
entry-vs-public, capability, test-scenario, dynamic-field-exists, transfer-composability,
vector-literal).

## Deepening round 3 — 4 beats (proven 2026-07-08)

Source: the third /kp-deepen round (`docs/deepening/round-3/`) — gap-seeded from the
experiment-4 recorded candidates plus the two carried promotion-rule deferrals; 15 tasks ×
2 models with the 86-claim pack loaded, gated by the same pinned binary
(`sui 1.74.1-8fc60f1fa966`, plain build). Triage table in `docs/deepening/round-3/triage.md`.
Two beats trace to on-target probe failures (territories 1 and 2); two were promoted on
recurrence per the rule recorded in `docs/deepening/round-3/territories.md` —
implicit-field-copy (exp-4 rental/kp61 + round-3 import-2/haiku) and param-mut (the exp-3
E04024 record + round-3 generic-3/haiku).

| beat | red form tried | observed (exit + key output) | classification | fragment (expected_error.txt) |
|---|---|---|---|---|
| missing-module-import | `event::emit(Ping { value })` with no `use sui::event` in the module | exit 1, `error[E03006]: unexpected name in this position` — the unresolved-alias variant | RED/GREEN pair | `Could not resolve the name 'event'` |
| destructure-ignore | `let Crate { id: _ } = c;` — `field: _` ignore of a `UID` field | exit 1, `error[E05001]: ability constraint not satisfied` — the ignore variant | RED/GREEN pair | `The type 'sui::object::UID' does not have the ability 'drop'` |
| implicit-field-copy | `let gem = p.gem;` where `Gem` has `store` only | exit 1, `error[E05001]: ability constraint not satisfied` — the implicit-copy variant (plus a downstream `E06001` unused value without 'drop' on the never-consumed struct) | RED/GREEN pair | `Invalid implicit copy of field 'gem' without the 'copy' ability` |
| param-mut | `public fun bump(c: Counter)` assigning `c.n = c.n + 1` through the non-`mut` parameter | exit 1, `error[E04024]: invalid usage of immutable variable` | RED/GREEN pair | `To use the variable mutably, it must be declared 'mut'` |

Notes:
- No new error *class* this round: `macros-2024` already pins E04024 (the assignment shape,
  fragment `Invalid assignment of immutable variable`); param-mut pins a new *message shape*
  under that existing class (the by-value-parameter shape). Also new message shapes under
  E03006 (the unresolved-alias variant — round 2's was the enum-construction variant) and
  E05001 (the ignore and implicit-copy variants — the pack now pins four distinct E05001
  shapes).
- missing-module-import is the *omission* sibling of round 1's use-self beat (which taught
  the lowercase-`self` form inside a `use` that exists); adjacency to the loaded events
  claim (which shows a fully-qualified `sui::event::emit` call in passing) is disclosed in
  the round-3 triage.
- Triaged-out candidates this round (reasons in `docs/deepening/round-3/triage.md`):
  `uid-reuse` (Sui E01001, 1 answer, deferred), `std-mem-replace` (E03002, 1 answer,
  deferred), `assert-abort-code` (0 hits this round, stays deferred), and import-2's
  E01002 — the round-2 taught class `block-statement-semicolon` recurring (a loaded rule
  ignored is recorded, not re-taught).
- Greens' `Move.lock` pin the same framework rev `b124567746b3a78a7e294ac2de265f693401ec9d`.

**Totals:** 35 green fixtures, 28 red fixtures (7 beats grounding-only: implicit-imports,
entry-vs-public, capability, test-scenario, dynamic-field-exists, transfer-composability,
vector-literal).

## Deepening round 4 — 4 beats (proven 2026-07-09)

Source: the fourth /kp-deepen round (`docs/deepening/round-4/`) — gap-seeded from the enriched
post-experiment ledger (experiment 5, payload-salience, sheet-confirm) plus the round-3
carried deferrals; 15 tasks × 2 models with the 98-claim pack loaded (payload byte-identical
to the confirmation draw's full arm, sha `4a53c7df…`), gated by the same pinned binary
(`sui 1.74.1-8fc60f1fa966`, plain build). Triage table in `docs/deepening/round-4/triage.md`.
Two beats trace to on-target probe failures in their own territories (compound-assignment,
std-mem-swap); one was promoted on recurrence per the pre-declared rule (borrow-arg-alias —
the sheet-confirm E07001 record + round-4 suimport-2/haiku); one is a new parse-level sibling
elicited inside the Rust-syntax territory (while-condition-parens).

| beat | red form tried | observed (exit + key output) | classification | fragment (expected_error.txt) |
|---|---|---|---|---|
| borrow-arg-alias | `consume(&mut p.pot, peek(&p.pot))` — a second borrow of the field inside the argument list of a call already holding `&mut` on it | exit 1, `error[E07001]: referential transparency violated` | RED/GREEN pair | `Field 'pot' is still being mutably borrowed by this reference` |
| compound-assignment | `t.total += n;` | exit 1, `error[E01002]: unexpected token` — `Unexpected '='`, `Expected an expression term` | RED/GREEN pair | `Unexpected '='` |
| while-condition-parens | `while i < n {` — Rust's paren-free loop head | exit 1, `error[E01002]: unexpected token` — `Unexpected 'i'`, `Expected '('` | RED/GREEN pair | `Expected '('` |
| std-mem-swap | `std::mem::swap(&mut d.slot, &mut old)` | exit 1, `error[E03002]: unbound module` | RED/GREEN pair | `Unbound module 'std::mem'` |

Notes:
- New error *class* this round: E07001 (referential transparency) — the pack's first. E01002
  gains two new message shapes (the compound-assignment `Unexpected '='` and the paren-free
  loop head `Expected '('` — round 2's was the missing-semicolon shape); E03002 gains the
  unbound-`std::mem` shape (round 3's std-mem-replace deferral, now proven in its `swap`
  variant after the family's third recorded answer).
- std-mem-swap-green teaches the replacement idiom, not just the absence: an `Option` slot
  with `std::option::swap(t: &mut Option<Element>, e: Element): Element` (doc claim grounds on
  the pinned framework-docs signature). The corpus gained one excerpt for borrow-arg-alias-doc:
  `reference/primitive-types/references.md` (Ownership — unique mutable borrows) from the SAME
  pinned move-book commit `8ce4dcb…` (no pin change).
- Triaged-out this round (reasons in `docs/deepening/round-4/triage.md`): gen-2/haiku's
  E04024 ×2 — the round-3 taught `param-mut` rule ignored while loaded (recorded, not
  re-taught); `vector-destroy-empty` (E06001, 1 answer, deferred); `vector-literal-annotation`
  (E04010, 1 answer, deferred).
- Three territories recorded clean with corners demonstrably exercised: sui-import-path (all
  six answers wrote `use sui::sui::SUI` — the ×4-cumulative top ledger class did not reproduce
  under targeted elicitation), generic-transfer-key-bound (all six bound choices sound; second
  consecutive clean probe), object-identity (all six answers passed with the identity
  corners engaged — `object::delete` ×4, `ID`-typed event fields; one registry keyed by the
  object's `address` form, noted in the triage).
- Greens' `Move.lock` pin the same framework rev `b124567746b3a78a7e294ac2de265f693401ec9d`.

**Totals:** 39 green fixtures, 32 red fixtures (7 beats grounding-only: implicit-imports,
entry-vs-public, capability, test-scenario, dynamic-field-exists, transfer-composability,
vector-literal).

## Deepening round 5 — 6 beats (proven 2026-07-10)

Source: the fifth /kp-deepen round (`docs/deepening/round-5/`) — the first designed by its own
mechanism experiment (`docs/experiments/sui-import-elicitation/`: incidental-shaped probes;
the sui-import beat pre-decided from the experiment's observed REDs). A pre-freeze adversarial
reviewer pass on the task audit is now a standing step (it returned REVISE and two drafts were
replaced BEFORE the freeze). Triage: `docs/deepening/round-5/triage.md`.

| beat | red form tried | observed (exit + key output) | classification | fragment (expected_error.txt) |
|---|---|---|---|---|
| sui-import | `use sui::coin::{Self, Coin, SUI}` | exit 1, `error[E03003]: unbound module member` | RED/GREEN pair | `Unbound member 'SUI' in module 'sui::coin'` |
| uid-to-address | `object::id_to_address(&inv.id)` on a `&UID` | exit 1, `error[E04007]: incompatible types` | RED/GREEN pair | `Invalid call of 'sui::object::id_to_address'. Invalid argument for parameter 'id'` |
| value-consumption-paths | `Coin` parameter consumed only in the winning branch of an `if` | exit 1, `error[E06001]: unused value without 'drop'` ("might still contain a value") | RED/GREEN pair | `The value does not have the 'drop' ability and must be consumed before the function returns` |
| vector-destroy-empty | drained `vector<Rocket>` left to drop at the closing brace | exit 1, `error[E06001]` ("still contains a value") | RED/GREEN pair | `The parameter 'rockets' still contains a value` |
| uid-vs-id | `object::id(&pet.id)` on the raw `UID` | exit 1, `error[E05001]: ability constraint not satisfied` | RED/GREEN pair | `The type 'sui::object::UID' does not have the ability 'key'` |
| empty-vector-annotation | `let owners = vector::empty();` with only `vector::length` downstream | exit 1, `error[E04010]: cannot infer type` | RED/GREEN pair | `Could not infer this type. Try adding an annotation` |

Notes:
- Two beats (`sui-import`, `uid-vs-id`) teach from held-out observed REDs under the frequency
  rule — their territories probed clean twice (round-4 focal, round-5 incidental); the rate
  ceiling (clean n=6 bounds p < ~0.3) is disclosed wherever those clean probes are cited.
- Both round-5 GREEN drafts initially violated the pack's own taught rules (a W99001
  transfer-to-sender and a deprecated `vector::empty()`) and were corrected to the pack
  idioms (Option-return; typed literal) before proving — the pack's rules now gate its own
  fixtures.
- The E06001 family now pins THREE shapes (option-field-fill's mutation, the branch-path
  "might still contain", the drained-vector "still contains"); E04007 pins table-key-by-value,
  type-name, and the id_to_address argument; E05001 reaches five shapes. Message-shape
  disclosure per the round-3 convention.
- Corpus extended with three excerpts from the SAME pinned commits (object.md identity
  signatures + std/vector.md destroy_empty from `d9f4797`; no pin change), and the
  sui-import-doc grounds on the donuts example's canonical import block already in the corpus.
- Greens' `Move.lock` pin the same framework rev `b124567746b3a78a7e294ac2de265f693401ec9d`.

**Totals:** 45 green fixtures, 38 red fixtures (7 beats grounding-only, unchanged).
