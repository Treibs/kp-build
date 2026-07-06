module macros_2024_red::demo {
    /// Pre-2024 style: rebinding a local declared without `mut`.
    public fun sum_to(n: u64): u64 {
        let total = 0;
        let i = 0;
        while (i < n) {
            total = total + i;
            i = i + 1;
        };
        total
    }
}
