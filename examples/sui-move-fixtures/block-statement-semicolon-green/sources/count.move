module block_statement_semicolon_green::count {
    // A braced `if` used as a statement mid-sequence is separated from
    // the next statement with `;`, like every other sequence item.
    public fun clamp(mut x: u64, cap: u64): u64 {
        if (x > cap) { x = cap };
        x
    }
}
