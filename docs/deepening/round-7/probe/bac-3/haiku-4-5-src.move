module fishing_boat::boat {
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use std::vector;

    public struct Box has key, store {
        id: UID,
        balance: Balance<SUI>,
        crew: vector<address>,
    }

    public struct AdminCap has key, store {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        let box = Box {
            id: object::new(ctx),
            balance: balance::zero(),
            crew: vector[],
        };
        transfer::share_object(box);

        let admin_cap = AdminCap {
            id: object::new(ctx),
        };
        transfer::transfer(admin_cap, ctx.sender());
    }

    public fun add_to_catch(box: &mut Box, payment: Coin<SUI>) {
        let coin_balance = coin::into_balance(payment);
        balance::join(&mut box.balance, coin_balance);
    }

    public fun sign_crew(box: &mut Box, deckhand: address) {
        vector::push_back(&mut box.crew, deckhand);
    }

    public fun pay_crew(
        box: &mut Box,
        _admin_cap: &AdminCap,
        ctx: &mut TxContext
    ) {
        let crew_size = vector::length(&box.crew);
        assert!(crew_size > 0, 0);

        let total = balance::value(&box.balance);
        let share = total / (crew_size as u64);

        let mut i = 0;
        while (i < crew_size) {
            let deckhand = vector::borrow(&box.crew, i);
            let coin_share = coin::from_balance(
                balance::split(&mut box.balance, share),
                ctx
            );
            transfer::public_transfer(coin_share, *deckhand);
            i = i + 1;
        };

        box.crew = vector[];
    }

    public fun box_balance(box: &Box): u64 {
        balance::value(&box.balance)
    }

    public fun crew_size(box: &Box): u64 {
        (vector::length(&box.crew) as u64)
    }
}
