---
id: otw-init-doc
statement: A one-time witness cannot be constructed manually (attempting to is a compilation
  error); it is received as the first argument of the module initializer, and because
  `init` runs only once per module the OTW is guaranteed to be instantiated only once.
paper: ''
supporting_passage: 'The OTW cannot be constructed manually, and any code attempting
  to do so will result in a

  compilation error. The OTW can be received as the first argument in the

  [module initializer](./module-initializer). And because the `init` function is called
  only once per

  module, the OTW is guaranteed to be instantiated only once.'
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
  evidence: 'The OTW cannot be constructed manually, and any code attempting to do
    so will result in a

    compilation error. The OTW can be received as the first argument in th'
  checked: '2026-07-06'
execution: {}
grounding:
  source: sui-move-book
  supporting_passage: 'The OTW cannot be constructed manually, and any code attempting
    to do so will result in a

    compilation error. The OTW can be received as the first argument in the

    [module initializer](./module-initializer). And because the `init` function is
    called only once per

    module, the OTW is guaranteed to be instantiated only once.'
judgment: {}
---

A one-time witness cannot be constructed manually (attempting to is a compilation error); it is received as the first argument of the module initializer, and because `init` runs only once per module the OTW is guaranteed to be instantiated only once.

> The OTW cannot be constructed manually, and any code attempting to do so will result in a
compilation error. The OTW can be received as the first argument in the
[module initializer](./module-initializer). And because the `init` function is called only once per
module, the OTW is guaranteed to be instantiated only once.

— *grounding verified* via doc-corpus: The OTW cannot be constructed manually, and any code attempting to do so will result in a
compilation error. The OTW can be received as the first argument in th
