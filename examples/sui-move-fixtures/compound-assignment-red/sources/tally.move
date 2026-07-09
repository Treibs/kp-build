module compound_assignment_red::tally {
    // Move has no compound-assignment operators. Rust's `+=` does not
    // parse; the increment must be written out as `x = x + n`.
    public struct Tally has drop {
        total: u64,
    }

    public fun add(mut t: Tally, n: u64): Tally {
        t.total += n;
        t
    }
}
