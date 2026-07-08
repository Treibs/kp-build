module wrap::gifting {
    use std::string::String;

    public struct WrappedGift<T: key + store> has key, store {
        id: UID,
        item: T,
        recipient: address,
        note: String,
    }

    public fun wrap<T: key + store>(
        item: T,
        recipient: address,
        note: String,
        ctx: &mut TxContext,
    ) {
        let gift = WrappedGift { id: object::new(ctx), item, recipient, note };
        transfer::public_transfer(gift, recipient);
    }

    public fun unwrap<T: key + store>(gift: WrappedGift<T>, ctx: &mut TxContext) {
        let WrappedGift { id, item, recipient: _, note: _ } = gift;
        object::delete(id);
        transfer::public_transfer(item, ctx.sender());
    }
}
