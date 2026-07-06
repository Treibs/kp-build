module dynamic_fields_red::container {
    public struct Container has key {
        id: UID,
    }

    public fun create(ctx: &mut TxContext) {
        transfer::share_object(Container { id: object::new(ctx) })
    }

    public fun set(container: &mut Container, name: vector<u8>, value: u64) {
        // Fabricated API: dynamic fields live in `sui::dynamic_field`, not on `object`.
        object::add_field(&mut container.id, name, value);
    }
}
