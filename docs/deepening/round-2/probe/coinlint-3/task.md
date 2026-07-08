Write a Sui Move module `split::royalty` (edition 2024). A shared `RoyaltyPool` is created with
two fixed beneficiary addresses. Anyone may `contribute(pool, coin)` to add SUI to the pool. Each
beneficiary may call `claim(pool, ctx)` at any time to receive their half of the currently
unclaimed funds (track what each beneficiary has already been paid; abort if the caller is not a
beneficiary).
