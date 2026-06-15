---
cite_key: ackermann2026
title: Gradient Regularization Prevents Reward Hacking in Reinforcement Learning from
  Human Feedback and Verifiable Rewards
authors:
- Johannes Ackermann
- Michael Noukhovitch
- Takashi Ishida
- Masashi Sugiyama
year: 2026
venue: ''
arxiv_id: '2602.18037'
arxiv_version: ''
doi: ''
url: https://arxiv.org/abs/2602.18037
verified:
  exists: true
  status: verified
  via: arxiv
  canonical_title: Gradient Regularization Prevents Reward Hacking in Reinforcement
    Learning from Human Feedback and Verifiable Rewards
  match_score: 1.0
  checked: '2026-06-15'
key_contributions:
- Reframes reward-hacking mitigation as biasing policy updates toward regions where
  the reward is more accurate, via gradient regularization (GR) toward flatter optima
- Derives a theoretical link between reward-model accuracy and the flatness of an
  optimum at convergence, and shows KL-penalty reference resets implicitly perform
  GR
- Empirically GR beats a KL penalty, avoiding format over-focus in rule-based rewards
  and preventing hacking the judge in LLM-as-a-Judge tasks
---

## Key contributions

- Reframes reward-hacking mitigation as biasing policy updates toward regions where the reward is more accurate, via gradient regularization (GR) toward flatter optima
- Derives a theoretical link between reward-model accuracy and the flatness of an optimum at convergence, and shows KL-penalty reference resets implicitly perform GR
- Empirically GR beats a KL penalty, avoiding format over-focus in rule-based rewards and preventing hacking the judge in LLM-as-a-Judge tasks
