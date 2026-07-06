# Design notes — the load-bearing decisions

This document explains *why* the engine is shaped the way it is. It is the contributor companion to
[`README.md`](README.md) (what it does) and [`SPEC.md`](SPEC.md) (the package format): the invariants
that must survive any refactor, and the honest limits we state instead of paper over.

## 1. The honesty doctrine: probe, falsify, refresh

The tool's brand is that it can say **"don't build"** and **"it didn't help."** A knowledge-package
builder that always recommends building and always declares victory is a compute sink with a
progress bar. So honesty is not a report section — it is three mechanical checks at three points in
a package's life:

- **`probe` (before)** — a pre-build weakness screen. Score an *unaided* answer: fabricated or
  mislabeled citations, hedges (placeholder ids like `arXiv:2510.xxxxx` — the model admitting it
  can't recall a paper it knows exists), thin grounding, or staleness → BUILD. Clean, recent, real
  citations → SKIP, don't spend the compute. One sample is noisy exactly where the decision matters,
  so multi-sample aggregation is asymmetric by design, at the decision level: any sample the screen
  decides is BUILD decides the aggregate (weakness that clears the screen's bar in one sample can't
  be un-observed by a luckier draw), while SKIP must hold in *every* sample.
- **`falsify` (after)** — a post-build measurement that tries to *disprove* the package's value:
  score a package-loaded agent against the unaided one on a held-out task. Fail, and the verdict says
  DID NOT HELP; the recorded manifest keeps that verdict.
- **`refresh` (later)** — a staleness report. A package's value concentrates exactly where fields
  move fastest, so the same motion that justified building it guarantees it rots. `refresh` re-runs
  the build's citation-graph expansion from the verified spine and asks one checkable question: has
  work appeared that post-dates the build? Verification is a statement about the past; freshness is a
  statement about the present, and nothing inside an assembled package can testify to the present.

**The falsify circularity, stated plainly.** The two mechanical axes are structurally stacked toward
the package side. The KP prompt hands the agent the verified spine and instructs it to cite only
those papers — so KP precision ≈ 1.0 is *instruction-following*, not a finding. Spine adoption
(recall) is graded against the package's own paper set — the treatment is the answer key. What the
mechanical axes genuinely measure is (a) how much the *base* model fabricates, mislabels, and misses
(a real weakness measurement), and (b) that the package was correctly assembled and adopted. They
cannot show the package made the answer *better*. The one non-circular axis is the optional **blind
quality panel** — anonymized A/B comparisons of the two answers by fresh judges — and it enters the
verdict as a **veto only**: a panel that prefers the base answer overturns a mechanical "helps," but
a panel that prefers KP never manufactures one. A helps verdict must clear the axis that *can* fail
and must not rest on the axes that can't. Without a panel, the verdict sentence says so explicitly.

## 2. Fail-closed conventions: abstain, never guess

Every layer of the engine prefers "I don't know" to a coin flip, because a wrong verdict in either
direction is a lie the whole tool is built to avoid.

- **Tri-state verdicts.** Checks that can genuinely fail to run return `True` / `False` / `None`,
  never a defaulted boolean. `_is_real` returns `None` when the citation index is unreachable;
  passage grounding returns `None` when the passage is too short (or the text too large) to
  fuzzy-scan; `helped()` returns `None` when either side has nothing checkable. `None` is excluded
  from denominators — a rate-limit burst must neither inflate nor deflate precision.
- **Exit codes carry the tri-state.** `probe`, `falsify`, and `refresh` exit **0 / 1 / 3**
  (build-or-helps-or-fresh / skip-or-did-not-help-or-stale / INCONCLUSIVE), with **2 reserved for
  usage and IO errors** — a missing answer file
  is exit 2, never dressed up as an inconclusive verdict, and malformed input never surfaces as a raw
  traceback. Scripts can branch on the verdict without parsing prose.
- **Transient ≠ fabrication.** A citation the index couldn't resolve after retries is *unresolved*,
  not fake. The probe goes further: if the confirmed-real count is low *only because* some citations
  were unreachable, the verdict is INCONCLUSIVE — a network blip must not masquerade as "the model is
  thin here" and force a build.
- **Grounding downgrades honestly.** Numeric fidelity matters most in quoted passages (a paraphrase
  that changes a digit changes the claim), so when the digits in a passage can't be confirmed against
  the source text the match degrades to `None`/`unconfirmed` rather than passing on fuzzy word
  overlap. And a *source we don't hold* is `ungrounded-unreachable` — a coverage debt, stamped
  distinctly from `ungrounded` (checked and absent). Couldn't-check and checked-and-absent never
  share a stamp, and neither is ever laundered into `verified`.
- **A total index outage is INCONCLUSIVE, not a tie.** When nothing on either side could be checked,
  precision/f1 are 0-by-default, not earned — comparing them would produce a confident verdict from
  no evidence.

## 3. The pluggable verifier seam

A claim ships only when *some oracle* said yes — and the engine now has four oracle families behind
one interface. A `Verifier` turns a claim into a `Verification` whose `exists` is the universal ship
gate and whose `kind` records which oracle produced it:

| kind | oracle | question it answers |
|---|---|---|
| **citation** | arXiv / Crossref / OpenAlex + strict title match | does the cited paper exist, and is it the paper named? |
| **doc-grounding** | pinned offline corpus | does the quoted passage appear verbatim in the pinned source? |
| **execution** | a mechanical tool gate on an artifact | does running the artifact clear the asserted gate? |
| **judgment** | a blind, relative judge panel | did the panel prefer this answer over its baseline? |

Three seam rules are load-bearing:

- **Exactly one verification basis per node.** A claim carries a `paper` XOR an `execution` XOR a
  `grounding` XOR a `judgment` directive — the loader rejects more than one. Otherwise a claim could
  shop for its friendliest oracle, and a citation anchor could override a mechanical disproof. The
  complement: a claim's *own* verdict is authoritative, so a firing execution gate vetoes a verified
  citation on the same claim — a mechanical disproof outranks provenance.
- **Provenance ≠ soundness.** Doc-grounding proves the clause is *verbatim in a pinned source* — it
  does not prove the source is right, and the package says which one it has. Same for citations: a
  verified spine means the papers are real and correctly identified, not that they are correct.
- **Execution verifies mechanical fundamentals, not aesthetics.** An execution gate can check that a
  lint rule doesn't fire or an inspection passes; it cannot check taste. A directive marked
  `aesthetic` (or lacking a gate code) is `unverifiable` — the verifier never guesses "pass" for
  quality. Aesthetic claims route to the judgment verifier instead, which is relative by
  construction (§4).

## 4. Judge panel anti-fraud

Quality judgments are the easiest verdicts to fake, so the JudgeVerifier is built around what a fake
would look like:

- **Relative, never absolute.** A taste score with no baseline is non-reproducible and tautological
  ("the judge liked it"). The verifier requires *both* an answer and a baseline and only ever reports
  better / worse / tie between them. An empty answer (or baseline) is `unverifiable` — an empty
  string must never be able to "win."
- **Slot alternation.** Across the panel's rounds the verifier alternates which option occupies slot
  A. A purely position-biased judge — or a lazy fake that votes the same slot every round — nets to a
  tie. This is a *bias cancellation*, and it lives in **one place**: the JudgeVerifier. The build
  replays recorded panels through it, and `falsify --judge-rounds` re-tallies its recorded slot
  winners through the same class — one implementation of the alternation math, so the prompt emitter
  and the replayer can never drift and silently invert half a panel.
- **Even-length ≥ 2, enforced at every layer.** An odd or length-1 recorded panel can launder a
  one-sided vote into a verdict: the cheapest fake, `rounds: ["a"]`, would read as a clean win, and
  truncating one balancing vote turns a tie into judged-better. The loader rejects odd panels, the
  replay abstains on them (defense-in-depth for directly-constructed claims), and `judge_replay`
  raises on them — the gate holds even if one layer is bypassed.
- **Fresh judge per round.** Each panel prompt goes to a judge with no shared context. A judge that
  saw a previous round can de-anonymize the slots (it knows which answer was A last time), and the
  alternation guarantee collapses.
- **No vote is safer than a bad vote.** A judge that raises, returns junk, or answers outside
  `a`/`b`/`tie` contributes *no* vote — and a panel with no usable votes is a tie, never a win.

**The honest limit:** alternation is bias cancellation, **not tamper-resistance**. Recorded rounds
are author-supplied data and the build performs no provenance check on them — an author who fabricates
a *balanced* panel (wins in both slot positions) will pass. What the gates remove is the cheap fraud:
position bias, uniform fakes, and odd-panel laundering. Trusting the recorded panel is trusting the
package author, and the design says so rather than implying otherwise.

## 5. Determinism and injected transports

Everything nondeterministic is injected; everything the engine decides is replayable.

- **`get`, `runner`, `judge`, `sleep` are constructor/keyword parameters everywhere.** The citation
  verifier takes its HTTP `get`, the execution verifier its `runner`, the judgment verifier its
  `judge`, and retry backoff its `sleep`. Every verifier is pure logic over an injected transport, so
  the whole suite runs offline with fakes, and a test never sleeps for real.
- **No wall clock in engine decisions.** `refresh(as_of=...)` *requires* a caller-supplied date and
  never calls `today()` itself; the probe's recency rule takes `--as-of`. The CLI supplies the clock
  at the boundary — so a refresh report or a probe verdict is deterministic and replayable, and a
  test can set the clock to anything.
- **Recorded-panel replay.** The LLM panel runs once, during research; its per-comparison slot
  winners are recorded in the claim's `judgment.rounds`. The build replays them through the
  JudgeVerifier deterministically, so a rebuild is byte-identical — a live judge at build time would
  make the package unreproducible.
- **Atomic manifest writes.** The manifest holds the package's recorded falsification verdict, so it
  is written write-then-rename (`os.replace`): a crash mid-write truncates a temp file, never the
  record itself.

## 6. Supply chain: the pinned execution tool

The execution verifier's default runner shells out to the `hyperframes` CLI via `npx`, which fetches
from the npm registry at build time — a supply-chain surface the engine treats explicitly rather
than silently:

- **A pinned version plus a pinned integrity.** The runner pins an exact `hyperframes@<version>` and,
  before the first tool run in a process, compares the registry's `dist.integrity` (sha512) against a
  recorded value — trust-on-first-use, recorded when the pin was taken. Once per process, not per
  claim; a mismatch never sets the confirmed flag.
- **A mismatch refuses, it never degrades.** If the check can't confirm the recorded integrity, the
  runner raises and the ExecutionVerifier maps that to status `error` — an unverified claim, never a
  pass on an untrusted tool. Honest scope: the check and `npx`'s own fetch are two *separate*
  registry requests (a check/fetch gap), so a registry that answers them differently defeats it, and
  it does not protect against a compromise that predates the pin. It raises the bar against a lazy
  later swap; it is not tamper-proof — the airtight path is the audited-binary escape hatch below.
- **`KP_BUILD_HYPERFRAMES_BIN` is the escape hatch.** Point it at a pre-audited local binary and the
  runner executes that directly, skipping both the download and the registry check — nothing is
  fetched, so there is no registry to distrust. Supplying an audited binary is the operator's
  explicit trust decision, not the engine's.

---

The common thread: every verdict states what was actually checked, every unchecked path is stamped
as unchecked, and every place the tool could quietly flatter itself is where a gate lives instead.
