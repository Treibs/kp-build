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
pip install -e ~/kp-build      # provides the `kp-build` CLI and the kp_build engine
```
Citation verification uses arXiv + Crossref (free, no key, network required).

## Procedure

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
  the statement must not reach past it (no added scope/numbers/certainty). **Honesty note:** the engine
  does NOT yet independently re-check that the passage actually appears in the paper — the claim is
  drafter-quoted, not machine-grounded. So scope claims tightly and only quote text you actually read;
  do not present these as independently verified. (A passage-presence gate is planned.)
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
kp-build build --input research.json --out <out_dir>
```
The engine **verifies every citation** (drops unverifiable ones + logs them), assembles the package,
generates `CONTEXT.md` (the agent payload), and lints. Read the output: any UNVERIFIED papers are a
signal a subagent may have hallucinated — investigate, don't ignore.

Research JSON:
```json
{"topic","scope",
 "papers":[{"cite_key","title","authors","year","venue","arxiv_id","doi","url","key_contributions"}],
 "claims":[{"id","statement","paper","supporting_passage","claim_type","confidence","corroborated_by"}],
 "open_problems":[{"id","statement","flagged_by","status","why_it_matters"}],
 "debates":[{"id","question","positions":[{"stance","papers","summary"}],"resolved"}]}
```

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
**recall** (fraction of the package's verified spine the answer used), reports an f1 verdict, and
writes it into `wikillm.json`. **If the KP answer does not beat base on f1 — especially if base's
hallucination rate is already ~0 because the model knows the topic — the package is not adding value;
say so and either pick a more model-weak topic or deepen the survey.** A `kp-build falsify` run is
also exposed via `eval/falsify.py` for convenience.

### 7 — Deliver
Hand over the package directory. Point the user at `CONTEXT.md` (load into an agent) and `README.md`
(human entry). State the citation-verification rate and the falsification result plainly. Confidence
is corpus-relative; the package is a *foundation*, not the paper.

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
