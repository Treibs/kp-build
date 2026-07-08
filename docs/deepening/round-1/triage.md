# Round-1 triage — sui-move

**Probe outcome:** haiku 7/15 pass (8 FAIL), sonnet 15/15 pass (7 clean, 8 with warnings).
Full per-task verdicts: `probe/results.txt`; raw compiler output per task: `probe/<task>/<model>.buildlog`.

All 8 failures are haiku's. They collapse into 5 root-cause families.

## Triage table

| task | model | observed error (pinned compiler) | verdict | reason |
|---|---|---|---|---|
| dynfields-3 | haiku | `error[E03003]` — "Invalid 'use'. Unbound member 'self' in module 'std::string'" | **beat-worthy** (→ `use-self`) | Wrong parametric syntax knowledge: Move group imports name the module with capital `Self`; lowercase `self` is the Rust idiom. No pack claim covers `use`-group syntax. |
| ptb-2 | haiku | `error[E03003]` — "Invalid 'use'. Unbound member 'self' in module 'sui::coin'" | **beat-worthy** (→ `use-self`) | Same root cause. |
| ptb-3 | haiku | `error[E03003]` — "Invalid 'use'. Unbound member 'self' in module 'std::option'" | **beat-worthy** (→ `use-self`) | Same root cause. |
| upgrades-2 | haiku | `error[E03003]` — "Invalid 'use'. Unbound member 'self' in module 'sui::balance'" | **beat-worthy** (→ `use-self`) | Same root cause. Four independent tasks, four territories touched — the highest-frequency residual gap in the probe. |
| security-1 | haiku | `error[E04007]` incompatible types — field `VecSet<String>` vs `type_name::get<T>()` "Given: 'std::type_name::TypeName'" | **beat-worthy** (→ `type-name`) | Wrong API-shape knowledge: `std::type_name::get<T>()` returns `TypeName`, not a string; model declared the storage field as `std::string::String`. Not covered by any pack claim. |
| upgrades-3 | haiku | `error[E04007]` (same TypeName/String mismatch) **and** `error[Sui E02005]` invalid one-time witness usage — "One-time witness types cannot be created manually" | **beat-worthy** (→ `type-name` + `witness-naming`) | Two independent gaps in one answer. The E02005: the model named its *plain* witness `MINTER` — the upper-case of module `minter` — which makes the compiler treat it as an OTW, and manual construction became illegal. The pack states what an OTW is (`otw-init`) but has no rule prescribing how NOT to collide with the naming convention. |
| ownership-1 | haiku | `error[E05001]` — "The type 'T' does not have the ability 'key'" (generic `unlock<T: store>` then `public_transfer(item, …)`) | **not beat-worthy** | Rule already loaded: `ownership-transfer-green` states verbatim that `public_transfer<T: key + store>` requires both abilities. The model ignored a loaded rule; a restated rule is not a new rule. Recorded, not taught. |
| ownership-2 | haiku | `error[E05001]` — "Invalid field type. The struct was declared with the ability 'key' so all fields require the ability 'store'" (`posts: vector<Post>`, `Post` with no abilities) | **beat-worthy** (→ `key-field-store`) | Wrong/missing parametric knowledge of the field-ability rule: every field of a `key` struct must have `store` (including vector element types). No pack claim covers field-ability requirements — `abilities` only pins the `id: UID` first-field rule. |

## Warning-tier triage (both models; the pack's shipped cleanliness axis)

Counted across all 30 buildlogs (`grep 'warning\['`, ANSI stripped):

| warning | count | root cause | verdict |
|---|---|---|---|
| `W04037` deprecated: `sui::dynamic_field::exists_` → "Renamed to \`exists\`" | 6 | Stale API name — 1.74.1 renamed it; both models still write `exists_` | **beat-worthy** (→ `dynamic-field-exists`, warning-tier: grounding-only green, like `entry-vs-public`) |
| `W04037` deprecated: `std::type_name::get` → "Renamed to \`with_defining_ids\`" | 6 | Stale API name | folded into the `type-name` beat's green/claims |
| `W04037` deprecated: `std::vector::empty` → "Use \`vector[]\` literal instead" | 3 | Stale idiom | recorded, **deferred to a future round** (small, edition-syntax corner; keeping round 1 scoped) |
| `Lint W99001` non-composable transfer to sender | 5 | Design-lint (pack has no composability beat) | recorded, deferred — same zone experiment 2 flagged on kiosk |
| `W09002` unused variable | 7 | One-off carelessness | not beat-worthy |
| `Lint W99010` unnecessary `entry` on `public` | 2 | Already covered (`entry-vs-public` beat); rule ignored | not beat-worthy (restated) |
| `Lint W99002` unenforceable custom transfer/share/freeze policy | 1 | Design-lint, single occurrence | not beat-worthy this round |

## Round-1 beats to teach (5)

| beat | fixes probe failures | class pinned |
|---|---|---|
| `use-self` | dynfields-3, ptb-2, ptb-3, upgrades-2 | E03003 "Invalid 'use'. Unbound member 'self'" |
| `type-name` | security-1, upgrades-3 (partial) + 6 deprecation warnings | E04007 TypeName/String mismatch; `get` → `with_defining_ids` rename |
| `witness-naming` | upgrades-3 (partial) | Sui E02005 invalid one-time witness usage |
| `key-field-store` | ownership-2 | E05001 key-struct field lacking `store` |
| `dynamic-field-exists` | 6 deprecation warnings (warning-tier) | W04037 `exists_` → `exists` rename (grounding-only: a warning cannot fail the red gate) |

New error classes for the pack: E02005 and E04007, plus new message shapes under existing codes
(E03003's "Invalid 'use'" variant; E05001's field-type variant).

## Territory findings

- **PTB composition, dynamic fields, package upgrades, security idioms** — all four produced
  beat-worthy failures (dominated by the cross-cutting `use-self` gap plus `type-name`).
- **Object-owner patterns** — one beat-worthy failure (`key-field-store`); one failure that was a
  loaded-rule violation, not a knowledge gap.
- **sonnet residual weakness is warning-tier only** (12 warnings across 15 tasks; breakdown above —
  dominated by the stale-API deprecations). Consistent with the experiment-2 finding that sonnet's
  gap is idiom currency, not compile-pass. No sonnet failure was compile-tier, so no sonnet-only
  compile beats this round.
