module compound_assignment_green::tally {
    // The full form `x = x + n` is the only assignment Move parses.
    public struct Tally has drop {
        total: u64,
    }

    public fun add(mut t: Tally, n: u64): Tally {
        t.total = t.total + n;
        t
    }
}
