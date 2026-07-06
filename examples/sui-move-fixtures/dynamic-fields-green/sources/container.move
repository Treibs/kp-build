module dynamic_fields_green::container {
    use sui::dynamic_field;

    public struct Container has key {
        id: UID,
    }

    public fun create(ctx: &mut TxContext) {
        transfer::share_object(Container { id: object::new(ctx) })
    }

    public fun set(container: &mut Container, name: vector<u8>, value: u64) {
        dynamic_field::add(&mut container.id, name, value);
    }

    public fun get(container: &Container, name: vector<u8>): u64 {
        *dynamic_field::borrow(&container.id, name)
    }
}
