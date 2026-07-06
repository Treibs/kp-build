module test_only_red::counter {
    public struct Counter has key {
        id: UID,
        value: u64,
    }

    #[test_only]
    public fun create_for_testing(value: u64, ctx: &mut TxContext): Counter {
        Counter { id: object::new(ctx), value }
    }

    // Non-test code calling a `#[test_only]` function.
    public fun create_default(ctx: &mut TxContext): Counter {
        create_for_testing(0, ctx)
    }
}
