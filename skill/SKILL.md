---
name: kp-build
description: >-
  Build a wikillm knowledge package: a portable, citation-verified, agent-loadable research-landscape
  foundation for starting a PhD-level paper on a NARROW topic. You scope it, dispatch survey subagents
  that find real papers (by search AND citation-graph expansion), extract grounded claims + the open
  problems each paper flags + the field's debates, verify every citation against arXiv/Crossref (no
  hallucinated papers), and assemble a package whose CONTEXT.md another agent loads to inherit the field
  without re-running the research. Use when someone wants the literature foundation to begin original
  research — NOT for settled textbook knowledge the model already has (that adds nothing).
---

# kp-build — `/kp-build`

You are the orchestrator. The user gives a narrow research area; you map its frontier into a
**wikillm package** — a reusable, verified, agent-loadable knowledge asset. **You + subagents do the
judgment (find, read, extract, synthesize); the Python engine (`kp_build`) does the mechanical,
deterministic part: verify every citation, assemble, lint.**

**Why this is not kpm-build:** kpm-build distils *settled* knowledge into axioms — which the model
already has. kp-build targets the *frontier*: recent, specific, contested literature the model is
worst at. The value is (1) verified citations (no hallucinations), (2) the open-problems register
(where new work goes), and (3) compute amortization (build once, anyone's agent loads it).

## Non-negotiables
- **No hallucinated citations.** Every paper is checked against a real index; unverifiable papers are
  dropped. The engine enforces this — but draft cites with a real `arxiv_id` or `doi` so they verify.
- **Scope narrow.** One package = one paper-sized research area ("speculative decoding for LLM
  inference"), not a whole field ("LLM inference") and not one paper.
- **The open-problems register is the point.** Mine each paper's *future-work / limitations /
  conclusion* sections for what it says is unsolved. A package with no open problems is a failure.
- **Coverage is scope-relative and can be too shallow.** Fight "missed the seminal paper" with
  citation-graph expansion (step 2), and record what you searched so the gap is honest.

## Setup
```
pip install kp-build                                       # the `kp-build` CLI + engine (from PyPI)
# or, unreleased/from source:  pip install git+https://github.com/Treibs/kp-build.git
```
Citation verification uses arXiv + Crossref (free, no key, network required).

## Procedure

### 0 — Pre-screen (is this topic even worth building?)
A package only adds value where the model is WEAK; on topics it already knows, falsification TIES and
you'd burn ~0.5–1.5M tokens for nothing. So gate the build BEFORE spending — it's the cheapest gate and
it guards the largest cost:
1. Get the probe task: `kp-build probe --emit-prompt --question "<the research area>"`.
2. Dispatch 2–3 INDEPENDENT unaided agents with it (no package, no shared context); save each answer
   (`base1.txt`, `base2.txt`, …). One sample is high-variance exactly where the decision matters — the
   sleep example's false SKIP came from one clean-looking sample.
3. Score them: `kp-build probe --answer base1.txt --answer base2.txt` → **BUILD / SKIP / INCONCLUSIVE**
   (exit 0 / 1 / 3; a usage or file error is exit 2). Aggregation is asymmetric by design, at the
   decision level: any sample the screen decides is BUILD decides the aggregate (observed weakness can't
   be un-observed by a luckier draw); SKIP requires every sample's decision to be skip.
   - **BUILD** — the unaided model is weak here: it fabricates/mislabels citations, **HEDGES** (writes
     placeholder ids like `arXiv:2510.xxxxx` for work it can't recall — proof it knows of a frontier it
     can't name), or is too thin → proceed to step 1.
   - **SKIP** — it already cites real papers cleanly → a package would add ~zero value; tell the user and
     stop, or pick a more model-weak angle. (This is the same condition that made 3 topics TIE in
     falsification.)
   - **INCONCLUSIVE** — the citation index was unreachable (or too many cites went transient) during
     scoring → re-run once the network is back. If it stays inconclusive on a persistent outage, treat
     conservatively as BUILD rather than risk skipping a model-weak topic.

   For a **known fast-moving** topic, add `--as-of YYYY-MM` (today): an answer that cites only OLD work
   (nothing recent) then also reads as model-weak on the frontier. It's opt-in — off by default, because
   old cites are correct on a settled topic.
This reuses the falsification scorer (citation precision / hallucination rate) — no new judgment, ~29k
tokens for one base answer, and it converts "build and hope" into a measured go/no-go.

### 1 — Scope (the one human step)
Confirm with the user: the **narrow research area**, the **sub-questions** a paper's related-work
must answer, and **in/out of scope**. Keep it tight. This defines "done."

### 2 — Survey (find the REAL papers — search + citation graph)
Dispatch survey subagents. Each must return real papers with a verifiable handle:
`{cite_key, title, authors, year, venue, arxiv_id?, doi?, url, key_contributions[]}`.
**Do two passes, not one:**
- (a) **Search** — arXiv, Semantic Scholar, Google Scholar, the venue (NeurIPS/ICML/ACL/...) for the
  seed papers of the area.
- (b) **Citation-graph expansion** — for the seed papers, follow their *references* (what they build
  on) and their *citations* (what builds on them). This is how you catch the seminal paper a keyword
  search misses. Prefer the highly-cited and the most-recent. **Tool-backed:** once a first wave is
  built, run `kp-build expand <pkg_dir> [--direction both|references|citations]` — it returns the actual
  neighbor papers of the verified spine from Semantic Scholar (keyless), de-duped against what's already
  in the package. Relevance-filter those candidates against the scope (a judgment call — most are
  off-topic), verify the keepers, fold them in, and record how many you added in
  `coverage.papers_via_expansion` (the report surfaces it as survey depth).
Every `cite_key` must carry an `arxiv_id` or `doi` (or an exact title) so the engine can verify it.
If a subagent can't find a real handle for a paper, it does not get cited — drop it, don't invent one.

### 3 — Extract (per paper — grounded, INDEPENDENT of the drafter, like kpm-build)
For each paper, dispatch extraction. Return, each tied to a **verbatim passage** from the paper:
- **Claims** — its key results/methods/findings: `{id, statement, paper, supporting_passage,
  claim_type, confidence}`. The `supporting_passage` MUST be a near-verbatim quote from the paper and
  the statement must not reach past it (no added scope/numbers/certainty). **Grounding:** the engine
  CAN machine-confirm the passage is really in the paper — run `kp-build build --ground` (checks each
  passage against the arXiv abstract, free; `--ground-fulltext` checks ar5iv fulltext and can mark a
  passage `ungrounded`, which caps+flags the claim). A passage that grounds is verified, not just
  quoted — so still quote text you actually read; a fabricated quote gets flagged.
- **Open problems** — what THIS paper says is unsolved / future work / a limitation:
  `{id, statement, flagged_by:[cite_key], status, why_it_matters}`. This is the highest-value output.
- **Debate position** — if the paper takes a side on a contested question, note it.
- **Refuter (rigor, INDEPENDENT)** — for each surprising or high-stakes claim, dispatch a SEPARATE
  refuter given the claim + the beat's *other* sources (not the claim's own), prompted to BREAK it:
  *"find a concrete reason this is wrong, overstated, or contradicted by these other sources."* If it
  succeeds, set `survived_refuter: false` on the claim. The engine then caps that claim to low
  confidence and flags it (⚠) in `CONTEXT.md` and the report — surfaced, not silently dropped — so a
  reader sees the contested ones. Claims with no refuter run default `survived_refuter: true`.

### 4 — Synthesize
- Merge open problems that multiple papers flag (`flagged_by` grows — corroboration that it's real).
- Build the **debate map**: cluster opposing positions into `{question, positions:[{stance, papers,
  summary}]}`.
- Mark `corroborated_by` on claims that several independent papers support.

### 5 — Assemble (the engine — verifies + lints)
Write the research JSON (shape below) and run:
```
kp-build build --input research.json --out <out_dir> --ground       # --ground machine-confirms passages (step 3)
```
The engine **verifies every citation** (drops unverifiable ones + logs them), grounds passages,
assembles the package, generates `CONTEXT.md` (the agent payload), and lints. Read the output: any
UNVERIFIED papers are a signal a subagent may have hallucinated — investigate, don't ignore.
- **Large package hitting rate limits?** Add `--throttle 0.5` (adaptive backoff between checks). If some
  cites still come back `error` (rate-limited, not fake), re-run with `--reuse-verification` — it keeps
  the good verdicts in `<out_dir>` and re-checks only the errored ones (cheap; turns 25/39 → 39/39).

Research JSON (every `cite_key` referenced anywhere must exist in `papers`):
```json
{"topic","scope",
 "papers":[{"cite_key","title","authors","year","venue","arxiv_id","doi","url","key_contributions"}],
 "claims":[{"id","statement","paper","supporting_passage","claim_type","confidence","corroborated_by"}],
 "open_problems":[{"id","statement","flagged_by","status","why_it_matters"}],
 "debates":[{"id","question","positions":[{"stance","papers","summary"}],"resolved"}],
 "benchmarks":[{"id","name","paper","dataset","method","metric","value"}],
 "coverage":{"sub_questions":[...],"queries":[...]}}
```
Controlled vocabularies (the engine rejects others): `claim_type` ∈ {result, method, finding,
definition}; `confidence` ∈ {high, medium, low}; open-problem `status` ∈ {open, partially-addressed}.
Non-arXiv papers set `arxiv_id:""` and carry a real `doi` (verified via Crossref) — kp-build is not
arXiv-only.

### 6 — Falsify (the acceptance gate — does it actually help?)
Run the falsification harness. Build the two prompts and dispatch two answer subagents:
```python
from kp_build.falsify import make_prompts
p = make_prompts(out_dir, "<the research area>")   # p["base"] (no package) and p["kp"] (CONTEXT.md injected)
```
Each subagent writes a related-work paragraph + 3 open problems ending in a `## Citations` block.
Then score and RECORD the verdict into the manifest:
```
kp-build falsify <out_dir> --question "<area>" --base base_answer.txt --kp kp_answer.txt
```
This scores both answers on **precision** (cited papers that actually exist — checked live) and
**recall** (spine adoption — fraction of the package's verified spine the answer used), reports an f1
verdict, and writes it into `wikillm.json` (atomically; pass `--no-record` to experiment without
touching a committed package). **If the KP answer does not beat base on f1 — especially if base's
hallucination rate is already ~0 because the model knows the topic — the package is not adding value;
say so and either pick a more model-weak topic or deepen the survey.** A `kp-build falsify` run is
also exposed via `eval/falsify.py` for convenience.

**Add the blind quality panel (recommended — it is the non-circular axis).** The two mechanical axes
favor the KP side by construction (the KP agent was *told* to cite the spine it is graded on), so a
mechanical win certifies base weakness + package adoption, not answer quality. To measure quality:
```
kp-build falsify <out_dir> --question "<area>" --base base_answer.txt --kp kp_answer.txt \
  --emit-judge-prompts 6
```
Give each printed prompt to a **fresh** judge subagent (no shared context — a judge that saw a previous
round can de-anonymize the slots), collect the six one-word verdicts (A/B/TIE) *in order*, then re-run
the falsify command with `--judge-rounds a,b,tie,...`. A panel that prefers the base answer **vetoes**
the mechanical win (exit 1); a panel that prefers KP is recorded but never manufactures a win.

### 7 — Deliver
**Falsify BEFORE you report — always.** Step 6 is a prerequisite for the human report: `kp-build
report` refuses to render a package that has no falsification result (the report's headline is "does
it help?", and a report that can't answer it is incomplete). So the order is fixed: run the
falsification test (step 6) → then generate the report:
```
kp-build report <out_dir> -o report.html      # errors unless step 6 has been run
```
Hand over the package directory + the report. Point the user at `CONTEXT.md` (load into an agent) and
`report.html` / `README.md` (human entry). State the citation-verification rate and the falsification
verdict plainly. Confidence is corpus-relative; the package is a *foundation*, not the paper.

The build also emits a `knowledge.json` — the [0xLT/kpm](https://github.com/0xLT/kpm) package
contract — so the package is **distributable by kpm with no extra work**: kp-build builds the
content, kpm handles distribution. To share it (build once so nobody re-spends the compute):
```
cd <out_dir> && kpm doctor && kpm pack      # validate + write a shareable .tgz
# or publish <out_dir> as a tagged GitHub repo; consumers then run:
kpm add github:<owner>/<repo>#v0.1.0 && kpm compose
```
Override the package identity at build time with `--name @scope/name --version X.Y.Z --license …`;
otherwise it defaults to `@kp/<topic-slug>@0.1.0` and the publisher re-tags however they like.

## What this is not
Not a search-result list, not a one-shot report (it is a persistent, verified, reusable asset), and
not an oracle — it is the frontier as the literature states it, with every citation checked to exist.
