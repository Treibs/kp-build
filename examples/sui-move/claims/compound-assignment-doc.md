---
id: compound-assignment-doc
statement: The Move reference's canonical loop increments with the written-out form
  `i = i + 1` — no compound assignment appears anywhere in the reference's loop idioms.
paper: ''
supporting_passage: "    while (i < n) {\n        if (&v[i] == target) return option::some(i);\n\
  \        i = i + 1\n    };"
claim_type: method
confidence: high
corroborated_by: []
survived_refuter: true
grounded: unchecked
verified:
  exists: true
  status: verified
  kind: grounding
  via: doc-corpus
  canonical_title: ''
  match_score: 0.0
  evidence: "    while (i < n) {\n        if (&v[i] == target) return option::some(i);\n\
    \        i = i + 1\n    };"
  checked: '2026-07-10'
execution: {}
grounding:
  source: sui-move-reference
  supporting_passage: "    while (i < n) {\n        if (&v[i] == target) return option::some(i);\n\
    \        i = i + 1\n    };"
judgment: {}
---

The Move reference's canonical loop increments with the written-out form `i = i + 1` — no compound assignment appears anywhere in the reference's loop idioms.

>     while (i < n) {
        if (&v[i] == target) return option::some(i);
        i = i + 1
    };

— *grounding verified* via doc-corpus:     while (i < n) {
        if (&v[i] == target) return option::some(i);
        i = i + 1
    };
