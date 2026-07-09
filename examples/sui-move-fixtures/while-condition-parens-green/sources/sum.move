module while_condition_parens_green::sum {
    // The parenthesized `while (cond)` form is the Move 2024 syntax.
    public fun sum_to(n: u64): u64 {
        let mut i = 0;
        let mut s = 0;
        while (i < n) {
            s = s + i;
            i = i + 1;
        };
        s
    }
}
