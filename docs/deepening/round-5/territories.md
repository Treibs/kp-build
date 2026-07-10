# Round-5 territories — sui-move

**Seeding rule:** gap-seeded from the experiment-6 ledger, the round-4 remeasure ledger, and
the sui-import elicitation experiment's frozen action map (`docs/experiments/
sui-import-elicitation/`, merged `1a1067a`). Pack at round start: 110 claims (master
`1a1067a`; claims unchanged since `0cdb536`).

**Gate-1 approval:** operator approved the five territories + the elicitation experiment
2026-07-10 with full run-to-merge authorization ("Approve + run to merge … experiment →
verdict → probe → teach → remeasure → PR + ralph loops → merge, no further gates").

**Probe-shape directive (binding, from the elicitation experiment's branch-1 action):**
every probe task is **incidental-shaped** — the territory's corner is a side requirement of
a non-focal core mechanic, never the task's headline. Additionally, 9 of the 15 tasks carry
an incidental SUI-payment element and every answer runs through the committed import checker
(`docs/experiments/sui-import-elicitation/check_import.py`): the probe doubles as the
elicitation experiment's named replication test.

**SUI-import beat (pre-decided):** taught this round from the elicitation experiment's four
observed failing answers (wrong-module shape, exact `E03003: Unbound member 'SUI' in module
'sui::coin'`) — per the frozen action map, independent of what this probe elicits.

## Approved territories

| # | territory | seed (recorded evidence) | why parametric knowledge is suspect |
|---|---|---|---|
| 1 | `value-consumption-paths` (`vcp`) — a non-`drop` value (usually a `Coin` parameter) must be consumed on **every** path, including the no-op path | exp-6: E06001 ×3 sites / 2 kp110 answers (promoted on frequency); the round-4 remeasure's gen-2 residual is the adjacent drained-vector shape | Rust drops unconsumed values silently on every path; Move's linearity makes the *else* branch (or the absence of branches) a compile error. The model writes the happy path and forgets the value survives the other one |
| 2 | `vector-destroy-empty` (`vde`) — a `vector<T>` where `T` lacks `drop` must be consumed with `vector::destroy_empty` even after it is drained | round-4 probe gen-2 ×1 + remeasure recurrence → ×2, promoted | Rust drops an empty `Vec` silently; Move's ability system doesn't know the vector is empty at the drop site |
| 3 | `uid-vs-ID` (`uid`) — `object::id(&x)` needs `x: T, T: key` (not a raw `UID`); identity in events/tables is the copyable `ID`; succession must convert before delete | sheet-confirm ×1 + exp-6 carbon-retire/kp98 ×1 → ×2 cumulative; round-4's focal probe was clean — this round re-probes it incidental-shaped (the elicitation lesson applied) | three identity types with no Rust analogue; the `object::id(&id)` shape shows the model treating `UID` as the identity value itself |
| 4 | `namespace-paths` (`ns`) — framework containers/utilities live under `sui::` (`sui::table`, `sui::bag`, `sui::clock`), not `std::` | exp-6 book-club/kp110 `use std::table` ×1 (16-error cascade); family sibling of the taught round-2 `string-module-path` (std::string is real; std::table is not) | the std-vs-sui split is memorized per-module, not derived; one wrong prefix cascades into double-digit unbound errors |
| 5 | `api-argument-shapes` (`api`) — framework calls with wrong argument forms: `object::id_to_address` (takes `ID`), `coin::put`/`take` (operate on `Balance`, not `Coin` fields), arity with `ctx` | exp-6 ×2 (id_to_address E04007, coin::put-on-Coin) + round-3 api-arity-missing-ctx ×1 — three ×1s, one family | signature-level knowledge decays fastest; the model knows the function exists and guesses the argument shape from Rust-ish intuition |

## Deliberately excluded

- **SUI-import as a probe territory** — pre-decided as a beat from the experiment's observed
  REDs (above); the probe's import-checker sweep is replication measurement, not elicitation.
- **conditional single-answer classes from exp-6** (`std-table-path` is territory 4's seed but
  its ×1 sibling shapes stay deferred; `id-to-address-arg` folded into territory 5).
- **W-tier warning beats** — the standing negative result stands.
- **Payload-form work** — double-dead per the sheet-confirm verdict.

## Probe shape

15 fresh authoring tasks (3 per territory), ALL incidental-shaped, dual model
(`claude-haiku-4-5` primary, `claude-sonnet-4-6` secondary), current 110-claim pack loaded,
pinned `sui 1.74.1-8fc60f1fa966` gate, plus the committed import checker on every answer.
Task freshness audited against the 122 prior probe/experiment tasks (60 round-1..4 probes,
34 experiment tasks, 6 salience, 6 sheet-confirm, 16 elicitation) and the 39 fixture zones —
**with a pre-freeze adversarial reviewer pass on the audit** (the elicitation erratum's
commitment: three audit misses in two experiments means the author no longer freezes an
audit alone). The pass returned REVISE — two tasks replaced, one reworked, disclosures
extended — all applied before the freeze; the record is in `probe/README.md`.
Mechanical repair rule pre-declared in `probe/README.md` before any answer.
