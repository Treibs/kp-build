module test_only_green::counter {
    public struct Counter has key {
        id: UID,
        value: u64,
    }

    public fun create(ctx: &mut TxContext) {
        transfer::share_object(Counter { id: object::new(ctx), value: 0 })
    }

    #[test_only]
    public fun create_for_testing(value: u64, ctx: &mut TxContext): Counter {
        Counter { id: object::new(ctx), value }
    }

    #[test_only]
    public fun destroy_for_testing(counter: Counter) {
        let Counter { id, value: _ } = counter;
        id.delete();
    }

    #[test]
    fun test_create_for_testing() {
        let mut ctx = tx_context::dummy();
        let counter = create_for_testing(7, &mut ctx);
        assert!(counter.value == 7);
        destroy_for_testing(counter);
    }
}
