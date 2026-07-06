module ownership_transfer_green::item {
    public struct Item has key, store {
        id: UID,
    }

    public fun mint_to(recipient: address, ctx: &mut TxContext) {
        transfer::public_transfer(Item { id: object::new(ctx) }, recipient)
    }
}
