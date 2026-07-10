# Round-5 triage — sui-move

Probe: 15 incidental-shaped tasks × 2 models, pack-loaded (110 claims, payload sha
`92756d2d…`), pinned `sui 1.74.1-8fc60f1fa966`, plus the committed import checker on every
answer. **haiku 8/15, sonnet 14/15** ([probe/results.txt](probe/results.txt)). Eight failing
runs; every log root-caused in full.

## Import replication sweep (the elicitation experiment's named replication test)

**haiku 1/9, sonnet 0/9** import-fails on the coin-bearing tasks (the one hit: vcp-2, absent
shape). Against the experiment's incidental arm (3/8), this draw does **not** reproduce
held-out-like rates — by the experiment README's own commitment: *"if not, this was noise
and the record will say so."* The record now says so: one draw at 3/8 and one at 1/9 under
the same shape directive brackets a low per-answer rate with high draw variance; the
salience reading is NOT supported beyond the frozen branch action. The SUI-import beat still
ships (pre-decided on the ×6-cumulative held-out frequency — vcp-2 makes it ×6), and its
tier-1/tier-2 effect is now the measurable question, not the elicitation mechanism.

## Failures

| task / model | observed | verdict | reason |
|---|---|---|---|
| vcp-1 / haiku | E04024 — `coin::split(&mut payment, …)` on a non-`mut` `payment: Coin<SUI>` param | **not beat-worthy** | round-3 taught `param-mut` **ignored while loaded** (exact rule/fix; the family's most-fired event) |
| vcp-2 / haiku | E03003 ×2 + 12 cascades — `use sui::coin::{self, …}` lowercase group-`self` AND `SUI` used with no covering import (the checker's FAIL absent) | **not beat-worthy** (self) + **beat evidence** (import) | the `self` is round-1 taught `use-self` ignored while loaded (3rd consecutive appearance across recent draws); the absent `SUI` import is the **SUI-import class ×6 cumulative** — observed RED evidence for the pre-decided beat |
| vcp-3 / sonnet | E04007 — `if (…) { balance::join(…) } else { transfer::public_transfer(…) }` as one expression: branch types `u64` vs `()` | **not beat-worthy (deferred)** | NEW class `branch-type-mismatch` ×1: the *consumption* is correct on both paths (the vcp corner handled!); the failure is if/else-as-expression typing. One answer → standing deferral; round-6 candidate |
| vde-1 / haiku | E06002 — `transfer::public_transfer(package, package.addressee)`: `package` moves as argument 1, then arg 2 reads it | **not beat-worthy (deferred)** | NEW class `moved-value-arg-order` ×1 (hoist the field read before the move; not Rust-bleed — Rust rejects this too). One answer → deferred; round-6 candidate. The vde corner itself was unreached (the loop died first) |
| uid-3 / haiku | E04010 — `let mut owners = vector::empty();` unannotated, inference fails downstream at `vector::length(owners)` | **beat-worthy** (`empty-vector-annotation`) | the round-4 `vector-literal-annotation` class in its `vector::empty()` shape — **×2 answers cumulative → promoted** (round-4 gen-3 `vector[]` + this). One beat covers both spellings: annotate the empty vector |
| ns-2 / haiku | E01002 `Unexpected 'let' / Expected ';'` + E04024 non-`mut` var | **not beat-worthy** | BOTH errors are loaded rules ignored: round-2 `block-statement-semicolon` (exact shape) and the `let mut` rule (`macros-2024`/`param-mut` family). Recorded — a single answer ignoring two loaded rules |
| api-1 / haiku | E04007 — `object::id_to_address(&invitation.id)` fed a `&UID` | **beat-worthy** (`uid-to-address`) | **the seeded territory-5 corner fired exactly as recorded** — ×2 cumulative (exp-6 carbon-retire kp110 + here). `id_to_address` takes `ID`; UID→address is `object::uid_to_address`, object→address is `object::id_address` |
| api-3 / haiku | E06001 — `envelopes: vector<Envelope>` parameter (non-`drop` elements) not consumed | **beat evidence** | the promoted `value-consumption-paths` / drained-vector family firing in a fresh draw — counted with the exp-6 evidence backing territory 1/2's beats (see below) |

## Clean corners (recorded)

- **uid-vs-ID (territory 3): clean on the probe again, corners demonstrably engaged** —
  `object::id(&artifact)` on objects, `uid_to_inner`, `object::delete` all correct in the
  passing answers, under the incidental shape this time. Two probes (focal round-4,
  incidental round-5) both clean while held-out draws keep hitting it (×2) — the SUI-import
  profile. **Beat taught anyway** under the frequency rule, from the held-out observed REDs;
  clean-probe claims carry the standing rate ceiling (p < ~0.3 at n=6).
- **namespace-paths (territory 4): clean** — no `std::table`-family error in any run
  (ns-2's failures were loaded-rule-ignored events). The exp-6 ×1 stays deferred; rate
  ceiling applies.
- **vde mechanics**: vde-2/vde-3 passed both models with genuine drain loops; the
  `destroy_empty` corner did not fire in its own territory this draw (api-3 carries the
  family's fresh evidence instead).

## Beat list for this round (6)

| beat | evidence | RED source |
|---|---|---|
| `sui-import` | ×6 cumulative held-out (pre-decided by the elicitation action map; fixtures already proven) | own fixture, observed `Unbound member 'SUI' in module 'sui::coin'` |
| `uid-to-address` | ×2 (exp-6 + probe api-1) | own fixture, observed E04007 |
| `value-consumption-paths` | exp-6 ×3 sites/2 answers (promoted) + api-3 family evidence | own fixture, observed E06001 |
| `vector-destroy-empty` | ×2 promoted (round-4 probe + remeasure) | own fixture, observed E06001 |
| `uid-vs-id` | ×2 held-out (sheet-confirm, exp-6 carbon `object::id(&id)` E05001) | own fixture, observed E05001 |
| `empty-vector-annotation` | ×2 promoted (round-4 gen-3 + probe uid-3) | own fixture, observed E04010 |

Every RED fixture is minimized from the observed failing shapes and proven through the
pinned binary before commit; every `expected_error.txt` fragment is pasted from the
fixture's own observed oracle output (never from prior logs).
