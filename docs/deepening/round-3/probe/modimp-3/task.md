Write a Sui Move module `pool::tipjar` (edition 2024). A shared `TipJar` is created by a
performer and accumulates tips in a pooled SUI balance. Anyone can `tip` by supplying a
`Coin<SUI>` which is absorbed into the pool. The performer (and only the performer — use a
capability issued at creation) can `sweep` the entire accumulated balance out as a `Coin<SUI>`
sent to themselves. Provide a public read function returning the current pooled amount.
