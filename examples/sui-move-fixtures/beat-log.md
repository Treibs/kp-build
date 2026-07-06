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
