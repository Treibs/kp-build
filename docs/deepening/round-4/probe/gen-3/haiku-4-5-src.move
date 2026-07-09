module exchange::gifts {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::TxContext;
    use std::vector;

    public struct GIFTS has drop {}

    public struct Gift<T: store> has store {
        item: T,
        giver: address,
    }

    public struct OrganizerCap has key, store {
        id: UID,
    }

    public struct GiftPool<T: store> has key {
        id: UID,
        gifts: vector<Gift<T>>,
    }

    fun init(_witness: GIFTS, ctx: &mut TxContext) {
        let organizer_cap = OrganizerCap {
            id: object::new(ctx),
        };
        transfer::public_transfer(organizer_cap, ctx.sender());
    }

    public fun create_pool<T: key + store>(ctx: &mut TxContext) {
        let pool = GiftPool {
            id: object::new(ctx),
            gifts: vector[],
        };
        transfer::share_object(pool);
    }

    public fun deposit_gift<T: key + store>(pool: &mut GiftPool<T>, item: T, giver: address) {
        let gift = Gift {
            item,
            giver,
        };
        vector::push_back(&mut pool.gifts, gift);
    }

    public fun hand_out<T: key + store>(
        pool: &mut GiftPool<T>,
        index: u64,
        recipient: address,
        _cap: &OrganizerCap,
    ) {
        assert!(index < vector::length(&pool.gifts), 1);
        let gift = vector::remove(&mut pool.gifts, index);
        let Gift { item, giver: _ } = gift;
        transfer::public_transfer(item, recipient);
    }

    public fun gifts_remaining<T: key + store>(pool: &GiftPool<T>): u64 {
        vector::length(&pool.gifts)
    }
}
