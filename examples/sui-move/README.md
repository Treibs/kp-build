# Sui Move contract authoring (Move 2024 edition, mainnet toolchain)

*wikillm knowledge package (`@kp/sui-move-contract-authoring-move-2024-edition-mainnet`) — a research-landscape foundation.*

*verified against sui mainnet-v1.74.1 · snapshot 2026-07-06*

**Scope:** 

- 0/0 citations verified (arXiv/Crossref); source years n/a
- 61 claims · 0 open problems · 0 debates · 0 benchmarks
- dropped (unverified-anchored): {'claims': 0, 'open_problems': 0, 'debates': 0, 'benchmarks': 0, 'positions': 0, 'relations': 0}

**Load `CONTEXT.md` into your agent** to inherit this field without re-running the research. `index.json` is the machine-readable graph (nodes + edges); the subdirectories hold the notes.

## Distribution

This is a [0xLT/kpm](https://github.com/0xLT/kpm) knowledge package (`knowledge.json`). Publish it as a tagged GitHub repo, then any consumer installs it with kpm — no re-research:

```bash
kpm add github:<owner>/<repo>#v0.1.0
kpm compose            # composes into a vault; load CONTEXT.md into your agent
```

Confidence is corpus-relative (conditional on the cited sources). Built 2026-07-06; revision beat + deepening round 1 added 2026-07-07.

## The plain-terms story

Ask an AI for a Sui contract today and it may well write last year's Sui. The counter-contract proof: an unaided model writing a plain counter contract from parametric memory produced pre-2024-edition Move — `struct Counter` — which fails to compile on sui mainnet-v1.74.1 (visibility annotations are mandatory in the 2024 edition). One mechanical fix (`public struct`) and the same contract builds green. The pack is a receipt-backed cheat sheet: every rule already ran through the real compiler, and every rule ships with the broken form the model would otherwise write.

## The RED/GREEN two-sided gate

Each rule carries a GREEN fixture (must compile); 17 of 22 rules also carry a RED fixture (must FAIL with a pinned error fragment in `expected_error.txt`). The refresh mechanic: Sui ships a new mainnet toolchain every ~2 weeks (the full re-verify loop is specified in [CONTEXT.md](CONTEXT.md)). This is the first pack whose staleness check is mechanical in both directions — with one disclosed exception: the test-scenario beat's `#[test]` body is not compiled by the plain-build gate (see [claims/test-scenario-green.md](claims/test-scenario-green.md)).

## Falsification

Both experiments recorded honestly:

| | experiment 1 (representative tasks) | experiment 2 (harder tasks, pre-registered dual metric) |
|---|---|---|
| compile-pass | base 5/5 = kp 5/5 (ceiling — did not clear the ship rule) | base 4/5 = kp 4/5 (tie; both arms failed the Receiving\<T\> task identically, Sui E02009) |
| clean-compile (zero warnings) | post-hoc observation only: base ~6 warnings vs kp ~2 | **pre-registered: kp 3/5 > base 2/5 → ships under rule branch 2** |

Protocols: `docs/experiments/sui-compile-pass/` and `docs/experiments/sui-compile-pass-2/` (pre-registration committed before answers at `b9653b6`). Scope the shipping claim exactly: the pack improves modern-idiom cleanliness on the pinned toolchain; it does NOT raise raw compile-pass rate for claude-sonnet-4-6 at this difficulty. Known gap recorded: `transfer::receive`/`Receiving<T>` (no beat covered it; both arms failed it).

**Revision beat (2026-07-07).** That gap is now closed by the fixture-proven `receiving` beat, added *after* the falsification and clearly separated from it (the numbers above were measured on the 44-claim pack): `public_receive(&mut parent.id, ticket)` with `ticket: transfer::Receiving<T>` and `T: key + store` — RED: cross-module `transfer::receive` fails with `error[Sui E02009]: invalid private transfer call`, the exact error both falsification arms hit. Provenance in [`examples/sui-move-fixtures/beat-log.md`](../sui-move-fixtures/beat-log.md).

**Deepening round 1 (2026-07-07).** A structured residual-gap probe (15 fresh tasks across five unprobed territories, dual model, pack loaded, pinned oracle — protocol and ledger in `docs/deepening/round-1/`) surfaced 8 compile failures for claude-haiku-4-5 that collapsed to 5 root-cause families, of which 4 were beat-worthy (the 5th was a loaded rule ignored, recorded not taught); a 5th beat came from the warning-tier count. Each beat is fixture-proven against the pinned compiler before commit: `use-self` (Move group-import `Self` keyword), `type-name` (`TypeName` vs `String` + the 1.74.1 `get` → `with_defining_ids` deprecation), `witness-naming` (plain witnesses must not collide with the OTW naming convention, Sui E02005), `key-field-store` (every field of a `key` struct needs `store`, E05001), and `dynamic-field-exists` (grounding-only: the 1.74.1 `exists_` → `exists` rename, warning-tier). Pack grew 47 → 61 claims. Same honesty invariant as the revision beat: the falsification numbers above were measured on the pre-deepening pack; deepening beats are receipt-proven but their held-out effect is unmeasured until the next tier-2 falsification.

## What this pack does NOT do

Compiling + idiomatic is a floor, not a security review. This pack does not deploy (`sui-deploy` is a planned follow-on), does not cover client/TS SDK code (`sui-ts-sdk` planned), and does not audit economic safety (reentrancy-class reasoning, invariant audits).
