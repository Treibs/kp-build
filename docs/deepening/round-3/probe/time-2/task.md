Write a Sui Move module `timelock::strongbox` (edition 2024). `lock(deposit: Coin<SUI>,
unlock_at_ms: u64, heir: address, ctx, ...)` creates an owned `Strongbox` for the heir that
cannot be opened before an absolute wall-clock time given in MILLISECONDS since the epoch.
`open(strongbox, ..., ctx)` verifies the current on-chain wall-clock time has reached
`unlock_at_ms`, pays the full contents to the opener, and destroys the box. Use the correct Sui
mechanism for reading wall-clock milliseconds on-chain.
