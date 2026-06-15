---
cite_key: turok2026
title: 'DUEL: Exact Likelihood for Masked Diffusion via Deterministic Unmasking'
authors:
- Gilad Turok
- Chris De Sa
- Volodymyr Kuleshov
year: 2026
venue: ''
arxiv_id: '2603.01367'
arxiv_version: ''
doi: ''
url: https://arxiv.org/abs/2603.01367
verified:
  exists: true
  status: verified
  via: arxiv
  canonical_title: 'DUEL: Exact Likelihood for Masked Diffusion via Deterministic
    Unmasking'
  match_score: 1.0
  checked: '2026-06-14'
key_contributions:
- 'Flags that masked diffusion models lack proper likelihood evaluation: the ELBO
  is a loose bound and is computed under the training rather than test-time distribution'
- Introduces the DUEL framework unifying deterministic-position-selection MDM samplers
- Proves DUEL samplers admit exact likelihood computation under the test-time distribution,
  giving MDMs proper perplexity for the first time
---

## Key contributions

- Flags that masked diffusion models lack proper likelihood evaluation: the ELBO is a loose bound and is computed under the training rather than test-time distribution
- Introduces the DUEL framework unifying deterministic-position-selection MDM samplers
- Proves DUEL samplers admit exact likelihood computation under the test-time distribution, giving MDMs proper perplexity for the first time
