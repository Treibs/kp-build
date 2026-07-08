module param_mut_green::counter {
    // Assigning through a by-value parameter requires `mut` on the
    // parameter, same as `let mut` for locals.
    public struct Counter has drop {
        n: u64,
    }

    public fun bump(mut c: Counter): Counter {
        c.n = c.n + 1;
        c
    }
}
