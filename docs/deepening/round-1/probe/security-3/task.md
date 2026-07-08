Write a Sui Move module `bank::bank` (edition 2024). A shared `Bank` holds a pooled
`Balance<SUI>` plus per-user accounting in a `sui::table::Table<address, u64>`.
`deposit(bank, coin, ctx)` adds the coin to the pool and credits the sender's accounted balance;
entry `withdraw(bank, amount, ctx)` aborts with a named constant on insufficient accounted funds,
debits the account, takes `amount` from the pooled balance as a `Coin<SUI>`, and transfers it to
the sender.
