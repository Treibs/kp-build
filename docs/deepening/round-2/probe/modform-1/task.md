Write a Sui Move module (edition 2024) implementing a per-address rate limiter. A shared
`Limiter` object tracks, for each caller address, the epoch in which that address last called.
Provide an entry function `ping(limiter: &mut Limiter, ctx: &mut TxContext)` that aborts if the
sender has already pinged in the current epoch, and otherwise records the current epoch for the
sender. Include a function to create and share the `Limiter`.
