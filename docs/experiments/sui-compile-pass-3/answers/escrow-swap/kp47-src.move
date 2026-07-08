module atomic_swap {
    use std::option::{self, Option};

    public struct Escrow<A: key + store, B: key + store> has key {
        id: UID,
        party_a: address,
        party_b: address,
        item_a: Option<A>,
        item_b: Option<B>,
    }

    public fun create<A: key + store, B: key + store>(
        item_a: A,
        party_b: address,
        ctx: &mut TxContext,
    ) {
        let escrow = Escrow {
            id: object::new(ctx),
            party_a: ctx.sender(),
            party_b,
            item_a: option::some(item_a),
            item_b: option::none(),
        };
        transfer::share_object(escrow);
    }

    public fun deposit<A: key + store, B: key + store>(
        escrow: &mut Escrow<A, B>,
        item_b: B,
        ctx: &mut TxContext,
    ) {
        assert!(escrow.party_b == ctx.sender());
        assert!(option::is_none(&escrow.item_b));
        escrow.item_b = option::some(item_b);
    }

    public fun swap<A: key + store, B: key + store>(
        escrow: Escrow<A, B>,
    ): (A, B) {
        assert!(option::is_some(&escrow.item_a));
        assert!(option::is_some(&escrow.item_b));
        
        let Escrow { id, party_a: _, party_b: _, item_a, item_b } = escrow;
        let a = option::destroy_some(item_a);
        let b = option::destroy_some(item_b);
        
        object::delete(id);
        
        (a, b)
    }

    public fun cancel_by_party_a<A: key + store, B: key + store>(
        escrow: Escrow<A, B>,
        ctx: &mut TxContext,
    ): A {
        assert!(escrow.party_a == ctx.sender());
        assert!(option::is_some(&escrow.item_a));
        
        let Escrow { id, party_a: _, party_b: _, item_a, item_b: _ } = escrow;
        object::delete(id);
        option::destroy_some(item_a)
    }

    public fun cancel_by_party_b<A: key + store, B: key + store>(
        escrow: Escrow<A, B>,
        ctx: &mut TxContext,
    ): B {
        assert!(escrow.party_b == ctx.sender());
        assert!(option::is_some(&escrow.item_b));
        
        let Escrow { id, party_a: _, party_b: _, item_a: _, item_b } = escrow;
        object::delete(id);
        option::destroy_some(item_b)
    }
}
