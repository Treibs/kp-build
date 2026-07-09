module borrow_arg_alias_green::pool {
    // The read of the field is hoisted to a `let` before the call, so the
    // immutable borrow ends before `&mut p.pot` is created.
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
        let amount = peek(&p.pot);
        consume(&mut p.pot, amount)
    }
}
