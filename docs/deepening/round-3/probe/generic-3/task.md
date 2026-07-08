Write a Sui Move module `relay::baton` (edition 2024). A relay race for arbitrary cargo: `start<T>(
cargo: T, next: address, legs: u64, ctx)` creates a `Relay<T>` holding the cargo and sends it to
the first runner. Each runner calls `pass(relay, next, ctx)` to forward the whole relay to the
next address, decrementing the remaining leg count; `pass` aborts when no legs remain. The final
holder calls `finish(relay, ctx)`, which hands them the bare cargo and retires the relay object.
