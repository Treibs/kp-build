Write a Sui Move module `park::meter` (edition 2024). A shared `Meter` has a fixed price per
hour in MIST (set at creation). `park(meter, payment, hours, ctx)` takes a `Coin<SUI>`, verifies
it covers `hours` hours, keeps exactly the owed amount in the meter's collected pool, and
returns any overpayment to the payer. It issues the payer an owned `Permit` object recording the
paid-through hour count and the epoch of purchase. A city capability sweeps the collected pool.
