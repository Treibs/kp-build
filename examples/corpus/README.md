# Grounding corpora (pinned source text for `--ground-verify`)

These are the offline source texts the `DocGroundingVerifier` checks claim passages against. A file is
named `<source>.txt`, where `<source>` is the `grounding.source` key in a claim's directive. They are
**excerpts**, committed so the grounding packs re-build deterministically and offline from a clean clone.

| file | source | provenance / license |
|---|---|---|
| `RFC9110.txt` | RFC 9110 (HTTP Semantics) §9.2–9.3 | © 2022 IETF Trust and the document authors. Reproduced under the [IETF Trust Legal Provisions / BCP 78](https://trustee.ietf.org/license-info), which permit reproduction with attribution. Full text: <https://www.rfc-editor.org/rfc/rfc9110>. |
| `VariableWidthTransformers.txt` | *Variable-Width Transformers*, Wu et al., arXiv:2606.18246v1 (2026-06-16) | © the authors. The abstract is reproduced verbatim with attribution for research/grounding-demo purposes. Source: <https://arxiv.org/abs/2606.18246>. |

These excerpts are used only to demonstrate provenance grounding (is a quoted clause verbatim in the
source?). They are not redistributed as standalone works; each carries its origin above.
