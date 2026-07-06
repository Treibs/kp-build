# Grounding corpora (pinned source text for `--ground-verify`)

These are the offline source texts the `DocGroundingVerifier` checks claim passages against. A file is
named `<source>.txt`, where `<source>` is the `grounding.source` key in a claim's directive. They are
**excerpts**, committed so the grounding packs re-build deterministically and offline from a clean clone.

| file | source | provenance / license |
|---|---|---|
| `RFC9110.txt` | RFC 9110 (HTTP Semantics) §9.2–9.3 | © 2022 IETF Trust and the document authors. Reproduced under the [IETF Trust Legal Provisions / BCP 78](https://trustee.ietf.org/license-info), which permit reproduction with attribution. Full text: <https://www.rfc-editor.org/rfc/rfc9110>. |
| `VariableWidthTransformers.txt` | *Variable-Width Transformers*, Wu et al., arXiv:2606.18246v1 (2026-06-16) | © the authors. The abstract is reproduced verbatim with attribution for research/grounding-demo purposes. Source: <https://arxiv.org/abs/2606.18246>. |
| `sui-docs-concepts.txt` | Sui documentation excerpts (`docs/content`) | © Mysten Labs. Docs licensed CC-BY-4.0 (repo `LICENSE-docs`; code Apache-2.0). Excerpted from [MystenLabs/sui](https://github.com/MystenLabs/sui) @ `d9f4797dbdcc9c5ec019fa190b432ea0e1bc39c1`. |
| `sui-framework-docs.txt` | Sui framework module docs (`sui::coin`) | © Mysten Labs, Apache-2.0 (repo `LICENSE`). Excerpted from [MystenLabs/sui](https://github.com/MystenLabs/sui) @ `d9f4797dbdcc9c5ec019fa190b432ea0e1bc39c1`. |
| `sui-move-book.txt` | *The Move Book* excerpts (`book/`) | © Mysten Labs, Apache-2.0. Excerpted from [MystenLabs/move-book](https://github.com/MystenLabs/move-book) @ `8ce4dcb9a23bef62d4d7ffe5c36e7002845d4897`. |
| `sui-move-reference.txt` | The Move Reference excerpts (`reference/`) | © Mysten Labs, Apache-2.0. Excerpted from [MystenLabs/move-book](https://github.com/MystenLabs/move-book) @ `8ce4dcb9a23bef62d4d7ffe5c36e7002845d4897`. |

These excerpts are used only to demonstrate provenance grounding (is a quoted clause verbatim in the
source?). They are not redistributed as standalone works; each carries its origin above.
