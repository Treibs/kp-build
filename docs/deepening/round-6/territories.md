# Round-6 territories — sui-move

**Seeding rule:** gap-seeded from the experiment-7 and round-5 ledgers. Pack at round start:
128 claims (master `e5496b7`; claims unchanged since `1b85d58`).

**Gate-1 approval:** operator instruction 2026-07-10, "run round 6 and continue with manim
until tonight" — continuing the round-5 run-to-merge authorization.

**Design intent (the experiment-7 open question, addressed by design):** experiment 7 asked
whether round 5's tier-2 win owed to its *beat-selection method* (frequency-promoted classes,
two beats taught from held-out REDs) rather than pack size. Round 6 is therefore designed
**the old way on the selection axis**: beats come ONLY from failures this round's probe
elicits (the round-1..4 rule — no frequency-rule teaching from held-out REDs, however strong
the ledger evidence). Everything else stays at round-5 standards (incidental-shaped tasks,
pre-freeze audit reviewer pass, import sweep), so the tier-2 falsification of this round
(experiment 8) read against experiment 7 isolates the selection variable as cleanly as two
adjacent rounds can.

## Approved territories

| # | territory | seed (recorded evidence) | why parametric knowledge is suspect |
|---|---|---|---|
| 1 | `std-option-path` (`opt`) — `Option`/std types imported from `sui::` (`use sui::option`) | ×2 promoted (exp-4 rental/kp61, exp-7 stall-rental/kp128 — the kp128 arm's own failure) | the mirror image of the taught `sui-import`: std modules pulled under the `sui::` prefix; the loaded payload *implies* the right path (`std::option::swap` in claim text) but never pins it |
| 2 | `branch-type-mismatch` (`brm`) — `if/else` (or `if/abort`) used as an expression with mismatched branch types, incl. the `abort ECode;` trailing-semicolon shape | ×2 promoted (round-5 probe vcp-3/sonnet, exp-7 stall-rental/kp128) | Rust coerces `!`/never types in branches; Move's `abort e;` with a semicolon yields `()` where the other branch yields a value |
| 3 | `coin-split-shapes` (`csp`) — `coin::split` called by value and/or expected to return a pair | ×1 answer / 2 misconceptions at one site (round-5 remeasure vcp-2: `let (a, b) = coin::split(payment, …)`) | Rust's `split_at` returns a pair and consumes by value; Move's `coin::split(&mut self, amount, ctx)` mutates in place and returns only the split-off coin |
| 4 | `moved-value-arg-order` (`mva`) — a value moved as an earlier call argument, then read in a later argument (`transfer(package, package.addressee)`) | ×1 carried (round-5 probe vde-1), self-fixed once in the remeasure | argument evaluation order + linearity: the read must be hoisted before the move — a slip both Rust and Move reject, but the model writes it under multi-concern load |
| 5 | `api-arity-ctx` (`ctx`) — framework constructors called without their `ctx`/required tail argument (`coin::zero()`, `balance::zero` confusion) | ×1 carried since round 3 (import-2 `sui::coin::zero()` E04016); exp-7 escape-room/base's `Balance::zero()` shape is family-adjacent | ctx-threading is Sui-specific; every Rust intuition says a zero-constructor is nullary |

## Deliberately excluded

- **Frequency-rule beats** (teaching any ledger class from held-out REDs without a probe
  elicitation this round) — excluded BY DESIGN this round; see the design-intent paragraph.
  If a promoted-class territory probes clean here, it is recorded clean and NOT taught,
  even at ×2+ held-out evidence — the cost of the controlled comparison, accepted knowingly.
- Ignored-while-loaded events — recorded, never re-taught (standing rule).
- W-tier warning beats; payload-form work (standing negative results).

## Probe shape

15 fresh incidental-shaped tasks (3 per territory), dual model (`claude-haiku-4-5` primary,
`claude-sonnet-4-6` secondary), 128-claim pack loaded (payload sha `d9e414e7…`), pinned
`sui 1.74.1-8fc60f1fa966` gate, the committed import checker on every answer (replication
point #4). Freshness audited against the **143** prior tasks (75 round-1..5 probes + 40 experiment
tasks across experiments 1–7 + 6 salience + 6 sheet-confirm + 16 elicitation) and the 45
fixture zones at
`e5496b7` — with the standing pre-freeze adversarial reviewer pass; its record lives in
`probe/README.md`, written before any answer.
