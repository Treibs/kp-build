module object_new_red::item {
    public struct Item has key {
        id: UID,
        value: u64,
    }

    public fun create(ctx: &mut TxContext) {
        // Fabricated API: there is no way to mint a UID from raw bytes.
        transfer::transfer(Item { id: object::uid_from_bytes(b"1234"), value: 0 }, ctx.sender())
    }
}
