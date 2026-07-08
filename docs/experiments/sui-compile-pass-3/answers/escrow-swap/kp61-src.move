module escrow::atomic_swap {
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;
    use std::option::{Self, Option};

    public struct Escrow<T: key + store, U: key + store> has key, store {
        id: UID,
        creator: address,
        counterparty: address,
        item_a: Option<T>,
        item_b: Option<U>,
    }

    public fun create<T: key + store, U: key + store>(
        counterparty: address,
        item_a: T,
        ctx: &mut TxContext,
    ): Escrow<T, U> {
        Escrow {
            id: object::new(ctx),
            creator: ctx.sender(),
            counterparty,
            item_a: option::some(item_a),
            item_b: option::none(),
        }
    }

    public fun deposit<T: key + store, U: key + store>(
        escrow: &mut Escrow<T, U>,
        item_b: U,
        ctx: &TxContext,
    ) {
        assert!(ctx.sender() == escrow.counterparty, 0);
        assert!(option::is_none(&escrow.item_b), 1);
        escrow.item_b = option::some(item_b);
    }

    public fun swap<T: key + store, U: key + store>(
        escrow: Escrow<T, U>,
        ctx: &TxContext,
    ): (T, U) {
        assert!(ctx.sender() == escrow.creator || ctx.sender() == escrow.counterparty, 0);
        assert!(option::is_some(&escrow.item_a) && option::is_some(&escrow.item_b), 1);
        
        let Escrow { id, item_a, item_b, .. } = escrow;
        object::delete(id);
        (option::destroy_some(item_a), option::destroy_some(item_b))
    }

    public fun cancel<T: key + store, U: key + store>(
        escrow: Escrow<T, U>,
        ctx: &TxContext,
    ): (Option<T>, Option<U>) {
        assert!(ctx.sender() == escrow.creator || ctx.sender() == escrow.counterparty, 0);
        assert!(!(option::is_some(&escrow.item_a) && option::is_some(&escrow.item_b)), 1);
        
        let Escrow { id, item_a, item_b, .. } = escrow;
        object::delete(id);
        (item_a, item_b)
    }
}
