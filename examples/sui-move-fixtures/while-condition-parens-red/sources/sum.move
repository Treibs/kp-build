module while_condition_parens_red::sum {
    // Move 2024 requires parentheses around the `while` condition.
    // Rust's paren-free `while cond {` form does not parse.
    public fun sum_to(n: u64): u64 {
        let mut i = 0;
        let mut s = 0;
        while i < n {
            s = s + i;
            i = i + 1;
        };
        s
    }
}
