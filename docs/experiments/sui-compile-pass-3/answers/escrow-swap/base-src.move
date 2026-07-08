module swap_escrow::escrow {
    use sui::object::{Self, UID};
    use sui::tx_context::{Self, TxContext};
    use sui::option::{self, Option};

    public struct Escrow<T: key + store, U: key + store> has key {
        id: UID,
        item_a: Option<T>,
        item_b: Option<U>,
        party_a: address,
        party_b: address,
    }

    public fun create<T: key + store, U: key + store>(
        item_a: T,
        party_b: address,
        ctx: &mut TxContext,
    ): Escrow<T, U> {
        Escrow {
            id: object::new(ctx),
            item_a: option::some(item_a),
            item_b: option::none(),
            party_a: tx_context::sender(ctx),
            party_b,
        }
    }

    public fun deposit<T: key + store, U: key + store>(
        escrow: &mut Escrow<T, U>,
        item_b: U,
        ctx: &mut TxContext,
    ) {
        assert!(tx_context::sender(ctx) == escrow.party_b, 1);
        assert!(option::is_none(&escrow.item_b), 2);
        option::fill(&mut escrow.item_b, item_b);
    }

    public fun swap<T: key + store, U: key + store>(
        escrow: Escrow<T, U>,
    ): (T, U) {
        let Escrow { id, mut item_a, mut item_b, party_a: _, party_b: _ } = escrow;
        object::delete(id);
        (option::extract(&mut item_a), option::extract(&mut item_b))
    }

    public fun cancel_by_party_a<T: key + store, U: key + store>(
        escrow: Escrow<T, U>,
        ctx: &mut TxContext,
    ): T {
        assert!(tx_context::sender(ctx) == escrow.party_a, 3);
        let Escrow { id, mut item_a, item_b: _, party_a: _, party_b: _ } = escrow;
        object::delete(id);
        option::extract(&mut item_a)
    }

    public fun cancel_by_party_b<T: key + store, U: key + store>(
        escrow: Escrow<T, U>,
        ctx: &mut TxContext,
    ): U {
        assert!(tx_context::sender(ctx) == escrow.party_b, 4);
        assert!(option::is_some(&escrow.item_b), 5);
        let Escrow { id, item_a: _, mut item_b, party_a: _, party_b: _ } = escrow;
        object::delete(id);
        option::extract(&mut item_b)
    }
}
