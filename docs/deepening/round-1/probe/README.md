# Round-1 probe — protocol and layout

**Arm: current pack loaded** (deepening probes measure *residual* gaps). There is no base arm;
tier-2 falsifications, not probes, are where base-vs-kp headline numbers come from.

## Protocol

- 15 tasks (3 per approved territory — see `../territories.md`), each in `<territory>-<k>/task.md`.
- Fresh context per task per model. Models (pinned IDs): `claude-haiku-4-5` (the pack's
  falsification primary), `claude-sonnet-4-6` (secondary).
- Prompt = task text + the single-code-block instruction + the pack payload (CONTEXT.md + all 47
  claim statements — same payload family as `docs/experiments/sui-compile-pass-2/`).
- Headless collection: `claude -p --tools ""` with the pinned model ID; raw output saved verbatim
  as `<model>.answer`.
- **Mechanical extraction (arm-neutral, same rule for every answer):** the first fenced code block
  is taken as the source (whole answer if unfenced) → `<model>-src.move`. No edits.
- **Scaffold repair (arm-neutral, pre-declared):** minimal `Move.toml` (edition 2024) binding every
  address name declared by the answer's own `module X::Y` lines to `0x0`. Extends the
  experiment-2 rule to multi-module answers; derived only from the answer text. No source touched.
- Gate: plain `sui move build` with the pinned binary (`sui 1.74.1-8fc60f1fa966`) — identical to the
  pack's fixture gate. Full output saved as `<model>.buildlog`; verdict in `<model>.result`:
  `PASS CLEAN` / `PASS WARN<n>` (n = `warning[` lines) / `FAIL <first error line>`.
  Committed buildlogs are ANSI-stripped and home-directory-redacted (`~`); verdicts were computed
  from the ANSI-stripped text. No compiler content was altered.
- Summary table: `results.txt`.

## Layout per task

```
<territory>-<k>/
  task.md            # the authoring task
  <model>.answer     # raw model output (verbatim)
  <model>-src.move   # extracted source (mechanical rule above)
  <model>-pkg/       # scaffold used for the gate (Move.toml + sources/)
  <model>.buildlog   # full pinned-compiler output
  <model>.result     # one-line verdict
```
