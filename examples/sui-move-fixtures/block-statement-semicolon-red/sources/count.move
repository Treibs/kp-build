module block_statement_semicolon_red::count {
    // Rust allows a braced statement without a trailing `;`; Move's
    // grammar requires the `;` between sequence items.
    public fun clamp(mut x: u64, cap: u64): u64 {
        if (x > cap) { x = cap }
        x
    }
}
