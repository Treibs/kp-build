# Round-3 probe — protocol and layout

**Arm: current pack loaded** (deepening probes measure *residual* gaps). There is no base arm;
tier-2 falsifications, not probes, are where base-vs-kp headline numbers come from.

This file is written and committed **before any answer is collected**.

## Protocol

- 15 tasks (3 per approved territory — see [`../territories.md`](../territories.md)), each in
  `<territory>-<k>/task.md`.
- **Held-out check (done before collection):** every task was checked against all prior task
  lists — the pack's fixture zones (31 as of master `322908a`), the round-1 and round-2 probes
  (30 tasks), and experiments 1/2/3/4 (22 tasks) — and restates none of them.
- **Elicitation design (pre-declared):** every task pins an explicit `module x::y` path — none of
  this round's territories targets the module-declaration form, so naming is controlled to keep
  failures isolated to the target corners (the round-2 asymmetry in reverse). Tasks are ordinary
  multi-concept authoring tasks that *invite* the territory's corner (module-function call sites,
  non-`drop` field dismantling, `Coin<SUI>`/`Option` signatures, generic transfers, epoch/ms
  time semantics); they never name the defect or hint at the rule.
- Fresh context per task per model. Models (pinned IDs): `claude-haiku-4-5` (the pack's
  falsification primary), `claude-sonnet-4-6` (secondary).
- Prompt = task text + the single-code-block instruction (verbatim from the round-1/2 probes and
  experiments 3/4) + the pack payload: `CONTEXT.md` + all 86 claim statements (Python `sorted()`
  byte order). The pack's claims and CONTEXT.md are unchanged since master `86989a1` (verified:
  the exp-4 merge touched only the pack README), so the payload is byte-identical to
  experiment 4's kp86 arm.
- Headless collection: `claude -p --tools ""` with the pinned model ID; raw output saved verbatim
  as `<model>.answer`.
- **Mechanical extraction (arm-neutral, same rule for every answer):** the first fenced code block
  is taken as the source (whole answer if unfenced) → `<model>-src.move`. No edits.
- **Scaffold repair (arm-neutral, pre-declared):** minimal `Move.toml` (edition 2024) binding every
  address name declared by the answer's own `module X::Y` lines to `0x0`; answers declaring only
  bare `module name {` forms get a single inert `probe = "0x0"` binding. Derived only from the
  answer text. No source touched. Multi-module answers gate as ONE package.
- Gate: plain `sui move build` with the pinned binary (`sui 1.74.1-8fc60f1fa966`) — identical to
  the pack's fixture gate. Buildlogs committed ANSI-stripped and home-directory-redacted; verdict
  in `<model>.result`: `PASS CLEAN` / `PASS WARN<n>` (n = `warning[` lines) / `FAIL <first error
  line>`. Summary in `results.txt`.

## Task index

| territory | tasks |
|---|---|
| 1 missing-module-import | modimp-1 (depot inventory, Table), modimp-2 (status beacon, events), modimp-3 (tip jar, Balance) |
| 2 destructure-ignore | destr-1 (piñata), destr-2 (bounty board), destr-3 (snake molt) |
| 3 wrong-module-import | import-1 (parking meter), import-2 (waitlist), import-3 (donation matcher) |
| 4 generic-transfer-key-bound | generic-1 (gift wrap), generic-2 (lost and found), generic-3 (relay baton) |
| 5 clock-epoch-confusion | time-1 (faucet cooldown), time-2 (ms timelock), time-3 (farm harvest) |
