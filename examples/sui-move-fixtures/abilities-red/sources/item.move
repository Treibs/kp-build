module abilities_red::item {
    public struct Item has key {
        value: u64,
    }

    public fun create(ctx: &mut TxContext) {
        transfer::transfer(Item { value: 0 }, ctx.sender())
    }
}
