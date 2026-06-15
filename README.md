# kp-build — citation-verified knowledge packages for agents

Build a **portable, citation-verified, agent-loadable** research-landscape package — the literature
foundation an agent needs to *begin* a PhD-level paper on a narrow topic. Built once, shared, so
nobody's agent re-spends the compute to reconstruct the field.

A package is a small directory: a **verified citation spine** (every paper checked live against
arXiv/Crossref — no hallucinated cites), an **open-problems register**, a **debate map**, **claims**
each anchored to a real source passage, and a token-bounded **`CONTEXT.md`** an agent loads to inherit
the topic. It's a reusable knowledge *asset*, not a one-shot "deep research" report — persistent,
structured, and machine-checkable.

> **When it pays off:** topics the model is *weak* on — recent / niche / post-training-cutoff. For
> topics the model already knows, a package adds traceability and reuse but not accuracy — and the
> built-in falsification gate will tell you so honestly, rather than sell you a hollow win.

## Install

```bash
pip install -e .            # the engine + the `kp-build` CLI
pip install -e '.[dev]'     # + pytest
```
Python ≥ 3.10. Runtime deps: `pyyaml`, `pydantic`. Citation verification hits the public
arXiv and Crossref APIs (no keys, no cost).

## Quickstart

`examples/` ships three real packages with their inputs, so you can run the engine end-to-end on a
clean clone. The engine's input is a `research.json` (papers, claims, open problems, debates):

```bash
# offline — assemble + lint without the network
kp-build build -i examples/discrete-diffusion-llms.research.json -o /tmp/pkg --no-verify

# live — verify every citation against arXiv/Crossref, and machine-ground each claim's passage
kp-build build -i examples/discrete-diffusion-llms.research.json -o /tmp/pkg --ground

# does the package actually help? score an unaided agent vs a KP-loaded agent (shipped answers)
kp-build falsify examples/discrete-diffusion-llms \
  --question "2024-2026 frontier of discrete/masked diffusion LMs" \
  --base examples/discrete-diffusion-llms.base-answer.txt \
  --kp   examples/discrete-diffusion-llms.kp-answer.txt

# render a self-contained HTML report (verdict, verified spine, open problems, debates)
kp-build report examples/discrete-diffusion-llms
```

Producing *your own* `research.json` for a new topic is the job of the **`/kp-build` skill**
(`skill/SKILL.md`), which orchestrates research subagents; the engine then does the mechanical,
deterministic part — verify, assemble, ground, lint, score.

## What the engine guarantees

- **No hallucinated citations (hard gate).** A paper is `verified` only when an explicit arXiv id or
  DOI resolves **and** its canonical title strictly matches. A "real id, wrong paper" mislabel fails.
  A title-only cite is `unconfirmed` and may not anchor a shipped claim. The gate never rescues a
  mismatched id with a title search.
- **Passage grounding (`--ground`).** Each claim quotes a source passage; grounding confirms that
  passage actually appears in the paper (the arXiv abstract for free, or ar5iv fulltext) — marking it
  `grounded`, `unconfirmed`, or `ungrounded` (fulltext-checked and absent → capped + flagged).
- **Falsification (the acceptance gate).** `kp-build falsify` scores a KP-loaded agent against an
  unaided base agent on a held-out task — on **precision** (cited papers that exist *and* match) and
  **recall** (coverage of the verified spine) → an f1 verdict recorded into the manifest. It refuses
  to claim a win the package didn't earn.
- **Topic-weakness probe (the go/no-go pre-screen).** `kp-build probe` scores one unaided base answer
  *before* you pay for a build: BUILD if the model fabricates, hedges (writes placeholder ids like
  `arXiv:2510.xxxxx` for work it can't recall), or is too thin; SKIP if it already cites cleanly.

## The three example packages

`examples/` ships three real packages built end-to-end, kept as reference output and regression
fixtures. Together they show what the probe and the falsification gate actually discriminate:

| package | topic regime | probe | falsification |
|---|---|---|---|
| `discrete-diffusion-llms` | model-**weak**, *fabricates* | BUILD | KP HELPS — wins on precision (kills mislabeled cites) **and** recall |
| `speculative-decoding-llms` | model-**known** | SKIP | KP helps on coverage only — precision already 1.0 |
| `rubric-based-rl-nonverifiable` | model-**weak**, *hedges* (2026) | BUILD | KP HELPS hugely — recall 0.07→1.00 |

See [`examples/README.md`](examples/README.md) for the full story (including how the rubric-RL example
exposed — and drove a fix for — a blind spot in the probe).

## Distribution — kp-build builds, [0xLT/kpm](https://github.com/0xLT/kpm) distributes

kp-build owns the **content** (research + verification + authoring); the open `0xLT/kpm` manager owns
**distribution** (install / lock / compose / pack / share). The seam is `knowledge.json`: every build
emits the kpm package contract, so a package *is* a first-class kpm package — "build once, share" is
the existing kpm CLI, no separate distribution layer.

```bash
kp-build build -i research.json -o ./pkg        # produces a valid kpm package
cd ./pkg && kpm doctor && kpm pack              # validate + write a shareable .tgz
# publish ./pkg as a tagged repo; any consumer then:
kpm add github:<owner>/<repo>#v0.1.0 && kpm compose   # inherits CONTEXT.md — no re-research
```

## Layout

```
src/kp_build/      the engine (scope→survey→extract→verify→ground→assemble→falsify→report)
skill/SKILL.md     the /kp-build orchestration spec (drives research subagents)
examples/          three real built packages + their research.json inputs and falsification evidence
docs/              explainer / metrics / orchestration (HTML)
SPEC.md            the package format + pipeline, in full
```

## Notes

- **Confidence is corpus-relative.** Every claim's confidence is conditional on its sources being
  right; the package says so rather than asserting absolute truth.
- **Coverage is scope-relative** and can be too shallow; citation-graph expansion mitigates it, and the
  manifest records what was searched so the gap is honest.
- A package is stale the day its field moves; the manifest carries `built`, and a re-run is a diff.

See [`SPEC.md`](SPEC.md) for the complete package format, schema, and pipeline.

## License

MIT — see [`LICENSE`](LICENSE). (Knowledge packages the tool *produces* default to CC-BY-4.0, set in
each package's `knowledge.json` and publisher-overridable.)
