---
id: block-statement-semicolon-red
statement: 'Omitting the `;` after a braced `if`/`while` statement mid-sequence (the
  Rust habit) fails to parse: sui 1.74.1 reports error[E01002] unexpected token —
  the next token is flagged with "Expected '';''". Every sequence item before the
  final expression needs the semicolon separator.'
paper: ''
supporting_passage: 'sui 1.74.1 rejects `if (x > cap) { x = cap }` followed by a statement
  without a `;` between them, with exit 1, error[E01002]: unexpected token, Expected
  '';''.'
claim_type: finding
confidence: high
corroborated_by: []
survived_refuter: true
grounded: unchecked
verified:
  exists: true
  status: verified
  kind: execution
  via: sui-move-build
  canonical_title: ''
  match_score: 0.0
  evidence: sui-move-build:red_violation cleared
  checked: '2026-07-08'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/block-statement-semicolon-red
grounding: {}
judgment: {}
---

Omitting the `;` after a braced `if`/`while` statement mid-sequence (the Rust habit) fails to parse: sui 1.74.1 reports error[E01002] unexpected token — the next token is flagged with "Expected ';'". Every sequence item before the final expression needs the semicolon separator.

> sui 1.74.1 rejects `if (x > cap) { x = cap }` followed by a statement without a `;` between them, with exit 1, error[E01002]: unexpected token, Expected ';'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
