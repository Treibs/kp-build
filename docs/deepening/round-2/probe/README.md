# Round-2 probe — protocol and layout

**Arm: current pack loaded** (deepening probes measure *residual* gaps). There is no base arm;
tier-2 falsifications, not probes, are where base-vs-kp headline numbers come from.

This file is written and committed **before any answer is collected**.

## Protocol

- 15 tasks (3 per approved territory — see [`../territories.md`](../territories.md)), each in
  `<territory>-<k>/task.md`.
- **Held-out check (done before collection):** every task was checked against all four prior task
  lists — the pack's fixtures, the round-1 probe (15 tasks), and experiments 1/2/3 (16 tasks) —
  and restates none of them. (Lesson from experiment 3, where this assertion turned out false for
  one task and had to be repaired with a sensitivity analysis.)
- **Elicitation design (pre-declared):** the three `modform-*` tasks deliberately do **not**
  dictate a module name or path — experiment 3 showed the E02004 bare-`module name {` defect fires
  exactly when naming is left to the model, and round-1's probe (which always supplied
  `module x::y` names) never saw it. All other territories pin the module path so their failures
  isolate to the target corner. This asymmetry is part of the design, not an accident.
- Fresh context per task per model. Models (pinned IDs): `claude-haiku-4-5` (the pack's
  falsification primary), `claude-sonnet-4-6` (secondary).
- Prompt = task text + the single-code-block instruction + the pack payload (CONTEXT.md + all 61
  claim statements, Python `sorted()` byte order — the identical payload family as
  `docs/experiments/sui-compile-pass-3/`'s kp61 arm; the pack's claims are unchanged since master
  `8c1a2e5`, so the payload is byte-identical to that experiment's).
- Headless collection: `claude -p --tools ""` with the pinned model ID; raw output saved verbatim
  as `<model>.answer`.
- **Mechanical extraction (arm-neutral, same rule for every answer):** the first fenced code block
  is taken as the source (whole answer if unfenced) → `<model>-src.move`. No edits.
- **Scaffold repair (arm-neutral, pre-declared):** minimal `Move.toml` (edition 2024) binding every
  address name declared by the answer's own `module X::Y` lines to `0x0`; if the answer declares
  **no** address name (bare `module name {`), the manifest carries a single inert `probe = "0x0"`
  binding so the gate can run — the binding references nothing in such answers and cannot rescue
  the declaration (counterfactual recorded at
  `docs/experiments/sui-compile-pass-3/e02004-counterfactual.buildlog`). Derived only from the
  answer text. No source touched.
- Gate: plain `sui move build` with the pinned binary (`sui 1.74.1-8fc60f1fa966`) — identical to the
  pack's fixture gate. Full output saved as `<model>.buildlog`; verdict in `<model>.result`:
  `PASS CLEAN` / `PASS WARN<n>` (n = `warning[` lines) / `FAIL <first error line>`.
  Committed buildlogs are ANSI-stripped and home-directory-redacted (`~`); verdicts are computed
  from the ANSI-stripped text. No compiler content is altered.
- Summary table: `results.txt`. Because territories 4–5 target warning-tier corners, the
  per-warning-code counts in PASS rows are triage inputs, not just the FAIL rows.

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
