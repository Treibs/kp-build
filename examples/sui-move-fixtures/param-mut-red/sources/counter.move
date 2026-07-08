module param_mut_red::counter {
    // Move 2024 requires the `mut` keyword on any binding that is
    // reassigned — including function parameters. Without `mut c`, the
    // assignment to `c.n` is invalid.
    public struct Counter has drop {
        n: u64,
    }

    public fun bump(c: Counter): Counter {
        c.n = c.n + 1;
        c
    }
}
