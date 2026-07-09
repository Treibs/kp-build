module exchange::gifts {
    public struct WrappedGift<T: store> has store {
        item: T,
        giver: address,
    }

    public struct GiftPool<T: store> has key {
        id: UID,
        gifts: vector<WrappedGift<T>>,
    }

    public struct OrganizerCap has key, store {
        id: UID,
    }

    public fun create<T: store>(ctx: &mut TxContext): OrganizerCap {
        let pool = GiftPool<T> {
            id: object::new(ctx),
            gifts: vector[],
        };
        transfer::share_object(pool);
        OrganizerCap { id: object::new(ctx) }
    }

    public fun deposit_gift<T: store>(pool: &mut GiftPool<T>, item: T, giver: address) {
        pool.gifts.push_back(WrappedGift { item, giver });
    }

    public fun hand_out<T: key + store>(
        _cap: &OrganizerCap,
        pool: &mut GiftPool<T>,
        index: u64,
        recipient: address,
    ) {
        assert!(index < pool.gifts.length());
        let WrappedGift { item, giver: _ } = pool.gifts.remove(index);
        transfer::public_transfer(item, recipient);
    }

    public fun gifts_remaining<T: store>(pool: &GiftPool<T>): u64 {
        pool.gifts.length()
    }
}
