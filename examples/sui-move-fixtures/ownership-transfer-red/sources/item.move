module ownership_transfer_red::item {
    public struct Item has key {
        id: UID,
    }

    public fun mint_to(recipient: address, ctx: &mut TxContext) {
        // `public_transfer` requires `store`; Item only has `key`.
        transfer::public_transfer(Item { id: object::new(ctx) }, recipient)
    }
}
