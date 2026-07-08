Write a Sui Move module `ledger::ledger` (edition 2024) with a shared `Ledger` object holding a
`sui::table::Table<address, u64>` of balances. Provide entry functions `credit(ledger, who, amount)`
which adds to (or creates) the entry for `who`, and `debit(ledger, who, amount)` which subtracts,
aborts with a named constant if the balance is insufficient or missing, and removes the table entry
entirely when it reaches zero. Create and share the Ledger in `init`.
