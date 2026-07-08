Write a Sui Move module `vend::machine` (edition 2024). A shared `VendingMachine` sells `Widget`
objects (a struct with `id: UID`) for a fixed `price: u64` in SUI and accumulates the proceeds
inside the machine. `buy(machine, payment, ctx)` accepts a `Coin<SUI>` worth at least the price,
keeps the price amount in the machine, returns any change to the buyer, and gives the buyer a
`Widget`. `collect(machine, cap, ctx)` lets the holder of a `MachineCap` withdraw all accumulated
proceeds.
