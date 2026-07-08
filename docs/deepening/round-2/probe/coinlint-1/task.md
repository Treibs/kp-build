Write a Sui Move module `pot::savings` (edition 2024). A `SavingsPot` is an owned object into
which the owner deposits SUI over time. `deposit(pot: &mut SavingsPot, coin: Coin<SUI>)` adds the
coin's value to the pot. `withdraw_all(pot: &mut SavingsPot, ctx: &mut TxContext)` pays the
entire saved amount out to the pot's owner (the transaction sender). Include a function that
creates a pot for the sender.
