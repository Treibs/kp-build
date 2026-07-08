module market::listing {
    use std::option::{Self, Option};
    use std::string::String;

    public struct Listing<T: store> has key {
        id: UID,
        item: Option<T>,
        note: String,
        seller: address,
    }

    public fun create<T: store>(item: T, note: String, ctx: &mut TxContext) {
        let listing = Listing {
            id: object::new(ctx),
            item: option::some(item),
            note,
            seller: ctx.sender(),
        };
        transfer::share_object(listing);
    }

    public fun cancel<T: store>(listing: &mut Listing<T>, ctx: &mut TxContext): T {
        assert!(listing.seller == ctx.sender());
        assert!(option::is_some(&listing.item));
        option::extract(&mut listing.item)
    }

    public fun relist<T: store>(listing: &mut Listing<T>, item: T, ctx: &mut TxContext) {
        assert!(listing.seller == ctx.sender());
        assert!(option::is_none(&listing.item));
        option::fill(&mut listing.item, item);
    }
}
