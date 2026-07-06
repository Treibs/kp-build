module test_scenario_green::counter {
    public struct Counter has key {
        id: UID,
        value: u64,
    }

    public fun create(ctx: &mut TxContext) {
        transfer::share_object(Counter { id: object::new(ctx), value: 0 })
    }

    public fun increment(counter: &mut Counter) {
        counter.value = counter.value + 1;
    }

    public fun value(counter: &Counter): u64 {
        counter.value
    }

    #[test]
    fun test_increment() {
        let mut scenario = sui::test_scenario::begin(@0xA);
        create(scenario.ctx());
        scenario.next_tx(@0xA);
        let mut counter = scenario.take_shared<Counter>();
        counter.increment();
        assert!(counter.value() == 1);
        sui::test_scenario::return_shared(counter);
        scenario.end();
    }
}
