# Round-4 probe — protocol and layout

**Arm: current pack loaded** (deepening probes measure *residual* gaps). There is no base arm;
tier-2 falsifications, not probes, are where base-vs-kp headline numbers come from.

This file is written and committed **before any answer is collected**.

## Protocol

- 15 tasks (3 per approved territory — see [`../territories.md`](../territories.md)), each in
  `<territory>-<k>/task.md`.
- **Held-out check (done before collection):** every task was checked against all prior task
  lists — the pack's fixture zones (35 as of master `a8cb8fc`), the round-1/2/3 probes
  (45 tasks), the remeasure reruns, and experiments 1–5 plus the payload-salience and
  sheet-confirm draws (34 tasks) — and restates none of them. Four draft candidates were
  **dropped by that audit**: a refundable event ticket (pay-then-refund restates sheet-confirm's
  bottle-deposit), a two-party generic swap meet (restates escrow-swap, experiments 1/3), a
  compound-key gradebook variant (restates the salience draw's grade-book), and a wishing well
  (restates round-3 modimp-3's tip jar / sheet-confirm's penalty-jar). Disclosed adjacencies
  kept (same standard as the sheet-confirm audit — adjacency named, mechanics differ):
  `suimport-3` (toll booth) shares "SUI accrues in a shared object" with round-3 modimp-3's tip
  jar but adds exact-price gating, a per-payment event, and a capped sweep; `rapi-3` (battery
  swap) shares "in-place component swap" with round-3 destr-3's snake molt but has no `Option`
  wrapper and *returns* the old part instead of discarding it; `gen-1` (prize award) shares
  "deposit an item another party takes" with round-3 generic-2's lost-and-found but awards via a
  judge capability to a declared winner rather than reclaim-by-describer; `oid-1` (card renewal)
  shares "object succession" with round-3 destr-3's snake molt but trades in the old object for
  a successor plus an identity-carrying event.
- **Elicitation design (pre-declared):** every task pins an explicit `module x::y` path (no
  territory targets the module-declaration form; naming is controlled to keep failures isolated
  to the target corners), and every pinned identifier passed the round-3 reserved-word check
  (`match`, `freeze`, `for`, `mut`, `enum`, `type` and friends avoided). Tasks are ordinary
  multi-concept authoring tasks that *invite* the territory's corner — `Coin<SUI>`/`Balance<SUI>`
  signatures with no import shown (T1), constructors that return values and counters that
  accumulate (T2), indexed vector scans / in-place component swaps / pairwise keys (T3), generic
  containers where the ability bounds are the model's choice (T4), object deletion, succession,
  and identity fields where UID/ID/address selection is the model's choice (T5); they never name
  the defect or hint at the rule.
- Fresh context per task per model. Models (pinned IDs): `claude-haiku-4-5` (the pack's
  falsification primary), `claude-sonnet-4-6` (secondary).
- Prompt = task text, then the single-code-block instruction (verbatim from the round-1/2/3
  probes and experiments 3–5): *"Answer with the complete Sui Move source only (edition 2024),
  in a single ```move code block. No explanations, no tools. If the task asks for two modules,
  put both in the same code block."* — then a line `--- Reference pack (verified) ---`, then the
  payload.
- **Payload:** the standard full payload (`CONTEXT.md` + `## Pack claims (all)`, sorted claim
  statements, one bullet each), **reused byte-identical** from the committed artifact
  `docs/experiments/sui-payload-salience/payloads/payload-full.md` — 49,656 bytes, sha256
  `4a53c7dfeb198aaca6df579c39be2adb697e01d40eeb0ff89ea6e000d39fbc4b`, re-verified at this
  round's freeze. Validity: `git diff 04d7cba..a8cb8fc` over `CONTEXT.md`, `claims/`, and
  `examples/sui-move.research.json` is empty, so the artifact equals the current 98-claim pack's
  payload. This is the recommended load form per the sheet-confirm verdict (the sheet is
  withdrawn); deepening probes load what answer-time loads.
- Headless collection: `claude -p --tools ""` with the pinned model ID, invoked from a neutral
  scratch working directory (not the repo — the experiment-4 protocol fix, kept ever since); raw
  output saved verbatim as `<model>.answer`.
- **Mechanical extraction (arm-neutral, same rule for every answer):** the first fenced code
  block is taken as the source (whole answer if unfenced) → `<model>-src.move`. No edits.
- **Scaffold repair (arm-neutral, pre-declared):** minimal `Move.toml` (edition 2024) binding
  every address name declared by the answer's own `module X::Y` lines to `0x0`; answers
  declaring only bare `module name {` forms get a single inert `probe = "0x0"` binding. Derived
  only from the answer text. No source touched. Multi-module answers gate as ONE package.
- Gate: plain `sui move build` with the pinned binary (`sui 1.74.1-8fc60f1fa966`) — identical to
  the pack's fixture gate. Buildlogs committed ANSI-stripped and home-directory-redacted;
  verdict in `<model>.result`: `PASS CLEAN` / `PASS WARN<n>` (n = `warning[` lines) /
  `FAIL <first error line>`. Summary in `results.txt`.

## Task index

| territory | tasks |
|---|---|
| 1 sui-import-path | suimport-1 (article paywall), suimport-2 (raffle pot), suimport-3 (toll booth) |
| 2 rust-syntax-bleed | rsyn-1 (scoreboard), rsyn-2 (pedometer), rsyn-3 (character XP) |
| 3 rust-api-bleed | rapi-1 (duel record), rapi-2 (leaderboard), rapi-3 (battery swap) |
| 4 generic-transfer-key-bound | gen-1 (prize award), gen-2 (care packages), gen-3 (gift exchange) |
| 5 object-identity | oid-1 (membership card renewal), oid-2 (pet adoption registry), oid-3 (demolition permit) |
