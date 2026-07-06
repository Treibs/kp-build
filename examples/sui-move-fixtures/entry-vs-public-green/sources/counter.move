module entry_vs_public_green::counter {
    public struct Counter has key {
        id: UID,
        value: u64,
    }

    // Plain `public fun` is PTB-callable; no `entry` needed.
    public fun create(ctx: &mut TxContext) {
        transfer::share_object(Counter { id: object::new(ctx), value: 0 })
    }

    public fun increment(counter: &mut Counter) {
        counter.value = counter.value + 1;
    }
}
