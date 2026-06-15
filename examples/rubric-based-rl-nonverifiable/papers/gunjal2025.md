---
cite_key: gunjal2025
title: 'Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains'
authors:
- Anisha Gunjal
- Anthony Wang
- Elaine Lau
- Vaskar Nath
- Yunzhong He
- Bing Liu
- Sean Hendryx
year: 2025
venue: ''
arxiv_id: '2507.17746'
arxiv_version: ''
doi: ''
url: https://arxiv.org/abs/2507.17746
verified:
  exists: true
  status: verified
  via: arxiv
  canonical_title: 'Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains'
  match_score: 1.0
  checked: '2026-06-15'
key_contributions:
- Introduces Rubrics as Rewards (RaR), the original on-policy RL method extending
  RLVR beyond verifiable domains using instance-specific rubric-based feedback as
  the reward signal
- Evaluates multiple strategies for aggregating multi-criterion rubric feedback into
  a scalar reward across medical and science domains (HealthBench, GPQA-Diamond)
- Best RaR variant beats Likert-based LLM-as-judge baselines (up to 31% relative on
  HealthBench, 7% on GPQA-Diamond) and improves alignment for smaller judges while
  reducing performance variance across judge scales
---

## Key contributions

- Introduces Rubrics as Rewards (RaR), the original on-policy RL method extending RLVR beyond verifiable domains using instance-specific rubric-based feedback as the reward signal
- Evaluates multiple strategies for aggregating multi-criterion rubric feedback into a scalar reward across medical and science domains (HealthBench, GPQA-Diamond)
- Best RaR variant beats Likert-based LLM-as-judge baselines (up to 31% relative on HealthBench, 7% on GPQA-Diamond) and improves alignment for smaller judges while reducing performance variance across judge scales
