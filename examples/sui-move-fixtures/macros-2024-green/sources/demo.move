module macros_2024_green::demo {
    /// Move 2024: single-argument `assert!`, `let mut`, labeled loops.
    public fun sum_capped(values: vector<u64>, limit: u64): u64 {
        let mut total = 0;
        let mut i = 0;
        'scan: loop {
            if (i >= values.length()) break 'scan;
            total = total + values[i];
            i = i + 1;
        };
        assert!(total <= limit);
        total
    }
}
