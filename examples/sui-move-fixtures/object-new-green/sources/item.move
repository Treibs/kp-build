module object_new_green::item {
    public struct Item has key {
        id: UID,
        value: u64,
    }

    public fun create(ctx: &mut TxContext) {
        transfer::transfer(Item { id: object::new(ctx), value: 0 }, ctx.sender())
    }
}
