# sui-move falsification — held-out compile-pass experiment

**Question:** does loading the pack raise the compile-pass rate of held-out Sui Move
contract-authoring tasks on the pinned mainnet toolchain (`sui 1.74.1-8fc60f1fa966`)?

**Answer: NO — both arms hit the ceiling.** base 5/5, kp 5/5. The pre-registered
metric could not discriminate. Under the ship rule (spec §6: *kp ≤ base → the pack
does not ship on this evidence*), this run does **not** clear the pack to ship.

## Protocol

See [`tasks.md`](tasks.md) for the 5 held-out tasks and the full protocol. In brief:
fresh context per task; **base** = task text only; **kp** = task text + pack
(CONTEXT.md + all claims); same model both arms (claude-sonnet-4-6); no compiler
access in either arm; answers dropped verbatim into an identical scaffold; scored by
`sui move build` with the pinned binary.

**Scaffold repair (arm-neutral, disclosed):** the original minimal `Move.toml` lacked
an `[addresses]` table, so any answer declaring a named address (all 10 did) failed on
*our* scaffold, not on its own code. We mechanically bound each answer's declared
address name to `0x0` — the same rule applied to every answer in both arms, derived
only from the answer's own `module X::Y;` line. No module source was touched.

**String redaction (disclosed):** both arms' task-2 answers happened to pick the same
project-internal name for the example token's display-metadata byte strings. Those
literal strings (token name/description only — no identifiers, no code) were replaced
with a neutral name before publication; both answers were recompiled after the edit
and their PASS results were unchanged.

## Results

| Task | base | kp |
|---|---|---|
| 1 shared-counter | PASS | PASS |
| 2 capped-token | PASS | PASS |
| 3 soulbound-badge | PASS | PASS |
| 4 escrow-swap | PASS | PASS |
| 5 guestbook-clock | PASS | PASS |
| **compile-pass** | **5/5** | **5/5** |

Raw log: [`results.txt`](results.txt). There were no FAILs, so there are no first-error
lines to record.

## Diagnosis (post-hoc, NOT a verdict)

The pre-registered metric saturated: claude-sonnet-4-6 already compiles all five of
these tasks unaided. The tasks were drawn to be *representative* contract shapes, and
representative turned out to be too easy for a compile-pass gate on this model.

A **post-hoc, non-pre-registered** observation, recorded for the next experiment's
design and explicitly *not* used as a shipping verdict: compiler warnings differed by
arm — base produced 6 warnings across its 5 answers (deprecated `use` idioms, lint
`W99001` non-composable transfer, `W99010` unnecessary `public entry`, one unused
constant); kp produced 2 (both `W04037` deprecated usage). Cleanliness looks like the
discriminating axis, but claiming it now would be exactly the post-hoc rationalization
the ship rule forbids. If it matters, it must be pre-registered and run on fresh tasks.

## Status

**Falsification NOT passed — not because the pack lost, but because the experiment
had no headroom.** Next step is an operator decision (harder held-out tasks, a
pre-registered clean-compile metric, a weaker base model, or accept and hold the
pack); recorded in the pack manifest as `verdict: ceiling`.
