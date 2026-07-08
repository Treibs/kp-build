Write a Sui Move module `match::donation` (edition 2024). A sponsor creates a shared `MatchPool`
funded with SUI reserves and naming a fixed charity address. `donate(pool, gift, ctx)` takes a
donor's `Coin<SUI>`, matches it 1:1 from the reserves when the reserves suffice (or matches
whatever remains when they don't), and forwards the combined amount to the charity address in
one payment. Provide a read function returning the remaining match reserves, and a sponsor-only
`refill` that adds more SUI to the reserves.
