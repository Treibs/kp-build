# sui-move-2024 — design spec

**Date:** 2026-07-06 · **Status:** draft for review · **Target:** `examples/sui-move-2024/` + `examples/sui-move-fixtures/`

## 1. What this pack is

A verified knowledge package that makes an agent write Sui Move contracts that **compile on
today's mainnet toolchain** and follow current (Move 2024 edition) idioms. It is the second
two-verifier pack after hf-kpmodel, pairing **execution** (the pinned `sui` compiler gates every
mechanical claim) with **doc-grounding** (every rule is anchored to a verbatim passage from
pinned official sources) — a different pairing than hyperframes' execution+judgment, so the seam
gains a new demonstrated combination.

**Model-weakness evidence (probe, 2026-07-06):** an unaided model writing a plain counter
contract from parametric memory produced pre-2024-edition Move — `struct Counter` — which
**fails to compile** on `sui` mainnet-v1.74.1 (visibility annotations are mandatory from the
2024 edition). One mechanical fix (`public struct`) and the same contract builds green. The
weakness is real, current, and the oracle discriminates cleanly.

**Why it matters (the shareable story):** ask an AI for a Sui contract today and it writes
last year's Sui. The pack is a receipt-backed cheat sheet: every rule already ran through the
real compiler, and every rule ships with the broken form the model would otherwise write.

## 2. Scope declaration (depth is set here)

- **Scope: contract authoring only** — the Move source that becomes the on-chain program.
- **Depth: thesis-depth within that scope.** The beat plan is decomposed from the deepest
  sources' own chapter structures (§4), not from an intro tutorial. The coverage label in the
  README is **relative to this declared scope**.
- **Explicitly out of scope for v1** (each is a planned follow-on pack, not a silent gap):
  - deploy + on-chain execution (`sui client publish`, PTBs, localnet) → `sui-deploy`
  - client/app code (TypeScript SDK, wallets, indexers) → `sui-ts-sdk`
  - economic/security auditing (reentrancy-class reasoning, invariant audits) — compiling and
    idiomatic is a floor, not a security review; the pack must say so
  - judgment layer (contract *design quality* via blind panel) — deferred until fundamentals
    are falsified

## 3. Verifiers exercised

| kind | oracle | what it proves |
|---|---|---|
| execution (primary) | `sui move build` exit 0 on the claim's fixture | the idiom is mechanically true on the pinned toolchain |
| doc-grounding (secondary) | verbatim passage in pinned local source file (offline, `--ground-verify`) | the rule is what the official docs say, not model paraphrase |

**RED/GREEN paired fixtures.** Every mechanical claim ships two Move packages under
`examples/sui-move-fixtures/<claim-id>/`:
- `green/` — minimal package that compiles clean and demonstrates the idiom
- `red/` — the naive-from-memory counterpart; **must fail** with the documented compiler error

The gate for a claim is two-sided: green builds (exit 0) **and** red fails with the expected
error snippet. A red that starts compiling on a newer toolchain is a *staleness signal*, not a
nuisance — it means the weakness the claim guards has healed and the claim should be retired.
This two-sided gate is the pack's honesty innovation over hf-kpmodel (whose gates are one-sided).

## 4. Beat plan (decomposed from the deepest sources)

Pinned sources (vendored excerpts, license-checked, commit-pinned in `CONTEXT.md`):

- **S1 — The Move Reference** (move-book.com/reference; MystenLabs/move-book) — deepest on
  language semantics and the 2024 edition
- **S2 — The Move Book** (move-book.com) — deepest pedagogical source on Sui-flavored Move
- **S3 — Sui docs, Concepts** (docs.sui.io; MystenLabs/sui `docs/content`) — object model,
  ownership, transaction semantics
- **S4 — Sui Framework API docs** (MystenLabs/sui `crates/sui-framework/docs`) — ground truth
  for framework calls

Beats, grouped by the source chapters they decompose from (≈16 claims; final list pinned during
the build after each beat's RED/GREEN pair is proven against the CLI):

**Part I — Move 2024 language (S1: edition guide + structs + functions chapters)**
1. Edition + struct visibility: `public struct` is mandatory (proven RED/GREEN 2026-07-06)
2. Method syntax: receiver functions + dot-call; positional structs
3. Implicit imports: `sui::object`/`sui::tx_context` aliases are implicit in 2024 — the
   legacy `use` block models emit is dead weight or an error (RED/GREEN to pin exact behavior)
4. Abilities (`key`/`store`/`copy`/`drop`) and what each permits for on-chain objects
5. Macros & loops as 2024 defines them (`assert!` without abort-code requirement, loop labels)

**Part II — Object model & ownership (S3: object model chapters; S2: objects part)**
6. Object creation: `UID`, `object::new(ctx)`, `key` requires `id: UID` first field
7. Ownership kinds: address-owned / shared / immutable / wrapped — and the transfer
   quartet `transfer` / `share_object` / `freeze_object` / `public_*` (`store`-gated)
8. `entry` vs `public` and PTB-callability (the compiler lints `public entry` as
   meaningless — observed on v1.74.1; models emit it habitually)
9. One-time witness + `init(witness, ctx)` shape
10. Capability pattern (`AdminCap`) as the access-control idiom

**Part III — Framework patterns (S4: coin, dynamic_field, event, clock modules)**
11. `Coin`/`Balance`/`TreasuryCap`: `coin::create_currency` with OTW
12. Dynamic fields vs dynamic object fields; `Table`/`Bag` and when each
13. Events: `event::emit`, event struct requirements (`copy, drop`)
14. `Clock` access (`&Clock`, `0x6`) — time is an object, not a syscall

**Part IV — Testing (S2: testing chapter; S4: test_scenario)**
15. `#[test]` + `test_scenario`: begin / next_tx / take_shared / return_shared lifecycle
16. `#[test_only]` modules and test-time object construction

Every beat gets: GREEN fixture, RED fixture with expected error, grounding passage (verbatim,
from the pinned source file), claim entry with `execution:` + `grounding:` blocks.

## 5. Oracle harness

- New execution tool in the verifier seam: `sui-move-build` (alongside the hyperframes runner).
  Runs `sui move build` in the claim's fixture dir; gate = exit code + expected-error match
  for RED.
- **Toolchain pin, mirroring the merged hyperframes pin:** `sui` release `mainnet-v1.74.1`,
  sha256 of the release asset TOFU-pinned once per process; `KP_BUILD_SUI_BIN` escape hatch;
  check/fetch TOCTOU documented as honest scope (same reviewed shape as the npm pin).
- Dependency note (honesty): `sui move build` resolves the framework from the toolchain's
  system packages; a fresh scaffold built successfully on this box on 2026-07-06, but **offline
  reproducibility was not proven** (no-network build not yet attempted). Prove it during the
  build; if a network fetch is observed, pin the framework rev in each fixture's `Move.toml`
  and document it.
- Grounding sources vendored as pinned local files (offline-only verification), with license +
  attribution recorded: MystenLabs/sui docs are Apache-2.0/CC-BY; move-book is CC-BY-4.0 —
  confirm exact licenses at vendoring time and attribute in `CONTEXT.md`.

## 6. Falsification (does it help?)

- **Held-out task set** (never appears in the pack): e.g. "shared counter with owner-gated
  reset", "fungible token with capped mint", "soulbound badge", "escrow swap between two
  objects", "timestamped guestbook using Clock". 5 tasks.
- Base agent answer vs KP-guided answer per task; **primary metric = compile-pass rate** on the
  pinned toolchain (the falsify execution axis), secondary = grounding f1 against the spine.
- Circularity note carries over from V2-c: mechanical spine scores measure adoption of the
  pack's own spine; compile-pass rate is the *non-circular* axis here (the compiler doesn't
  care what the pack says), which is a stronger position than citation packs enjoy.
- Exit-code doctrine unchanged: 0 helps / 1 did not help / 3 inconclusive; 2 usage/IO.
- If compile-pass rate doesn't move, the pack does not ship. Same rule as always.

## 7. Refresh story (this pack rots fast — by design, that's its value)

- Sui ships a new mainnet toolchain every ~2 weeks; `kp-build refresh` covers citation spines,
  not toolchains, so `CONTEXT.md` records toolchain version + docs commits, and the README
  documents the manual re-verify loop: bump pin → re-run all RED/GREEN gates → any RED that
  now compiles means the claim retires (healed weakness); any GREEN that breaks means the
  idiom moved.
- This "reds healing" mechanic is worth writing up in the README — it's the first pack whose
  staleness check is fully mechanical in both directions.

## 8. Deliverables

1. `examples/sui-move-2024/` — the package (claims, relations, CONTEXT.md, README.md)
2. `examples/sui-move-fixtures/` — RED/GREEN Move packages per claim + vendored pinned
   grounding sources
3. Verifier seam change: `sui-move-build` execution tool + tests (RED/GREEN two-sided gate,
   pin behavior, escape hatch) — same test discipline as the hyperframes runner (16/16 style)
4. Falsification run recorded in `wikillm.json` + README before/after story
5. Example README with the plain-terms value story (§1) and the honest caveat (§2)

## 9. Risks / open questions

- **Implicit-import exact semantics (beat 3)**: pin by experiment, not memory — the RED/GREEN
  build is the arbiter of whether legacy `use` lines warn, error, or pass silently.
- **Expected-error matching**: compiler error text changes across versions; match on stable
  error *codes/fragments* (e.g. the visibility-annotation sentence), keep fragments minimal.
- **Two-sided gate in the verifier**: `execution:` schema today encodes one gate; RED needs
  either a second directive or a `gate_code: red-fails` convention — decide in the plan, keep
  the schema change minimal and backward-compatible with hf-kpmodel.
- **Vendored doc licensing**: confirm at vendoring time; excerpts + attribution, not wholesale
  copies.
