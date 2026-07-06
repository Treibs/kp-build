module method_syntax_green::counter {
    public struct Counter has key {
        id: UID,
        value: u64,
    }

    public fun create(ctx: &mut TxContext) {
        transfer::share_object(Counter { id: object::new(ctx), value: 0 })
    }

    public fun value(self: &Counter): u64 {
        self.value
    }

    public fun is_zero(counter: &Counter): bool {
        counter.value() == 0
    }
}
