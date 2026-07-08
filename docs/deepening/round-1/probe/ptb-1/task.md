Write a Sui Move module `basket::basket` (edition 2024). A `Basket` is an object holding a
`Balance<SUI>`. Provide a non-entry `public fun new(ctx: &mut TxContext): Basket` designed to be
called as one command of a programmable transaction block, so a later PTB command can transfer the
returned basket. Also provide an entry function `deposit` that takes `&mut Basket` and a
`Coin<SUI>` by value and adds the coin's balance to the basket, and a public read function
returning the basket's current balance value as `u64`.
