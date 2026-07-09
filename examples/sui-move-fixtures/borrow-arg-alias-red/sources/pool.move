module borrow_arg_alias_red::pool {
    // A second borrow of a field inside the argument list of a call that
    // already holds `&mut` on that field violates unique ownership of
    // mutable references. Rust's two-phase borrows allow this ordering;
    // Move does not — the read must be hoisted before the call.
    public struct Pool has drop {
        pot: u64,
    }

    fun peek(x: &u64): u64 {
        *x
    }

    fun consume(x: &mut u64, amount: u64): u64 {
        *x = *x - amount;
        amount
    }

    public fun drain(p: &mut Pool): u64 {
        consume(&mut p.pot, peek(&p.pot))
    }
}
