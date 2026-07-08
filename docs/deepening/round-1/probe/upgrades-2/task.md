Write a Sui Move package (edition 2024) as two modules IN ONE ANSWER: `vault::core` and
`vault::api`. `vault::core` defines a `Vault` object storing a `Balance<SUI>` and a
withdraw helper that must be callable ONLY from modules inside the `vault` package (not from
other packages), returning a `Coin<SUI>`. `vault::api` provides the public entry function
`withdraw(vault: &mut Vault, amount: u64, ctx: &mut TxContext)` that uses the package-internal
helper and transfers the coin to the sender. Also give `vault::core` a public `deposit`.
