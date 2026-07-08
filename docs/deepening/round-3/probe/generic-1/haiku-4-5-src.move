module wrap::gifting {
    use std::string::String;

    public struct WrappedGift<T: store> has key, store {
        id: UID,
        item: T,
        note: String,
    }

    public fun wrap<T: store>(
        item: T,
        recipient: address,
        note: String,
        ctx: &mut TxContext,
    ) {
        let gift = WrappedGift {
            id: object::new(ctx),
            item,
            note,
        };
        transfer::public_transfer(gift, recipient);
    }

    public fun unwrap<T: store>(gift: WrappedGift<T>): T {
        let WrappedGift { id, item, note: _ } = gift;
        object::delete(id);
        item
    }
}
