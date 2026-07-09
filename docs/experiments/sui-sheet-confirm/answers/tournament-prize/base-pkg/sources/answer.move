module tournament::prize_pool {
    use sui::object::{Self, UID, ID};
    use sui::coin::{Self, Coin};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use std::vector;

    struct Tournament<phantom T> has key {
        id: UID,
        entry_fee: u64,
        start_epoch: u64,
        pool: Coin<T>,
        entrants: vector<address>,
    }

    struct OrganizerCap has key {
        id: UID,
        tournament_id: ID,
    }

    public fun create_tournament<T>(
        entry_fee: u64,
        start_epoch: u64,
        ctx: &mut TxContext,
    ): OrganizerCap {
        let tournament = Tournament {
            id: object::new(ctx),
            entry_fee,
            start_epoch,
            pool: coin::zero<T>(ctx),
            entrants: vector::empty(),
        };
        
        let tournament_id = object::id(&tournament);
        
        let cap = OrganizerCap {
            id: object::new(ctx),
            tournament_id,
        };
        
        transfer::share_object(tournament);
        cap
    }

    public fun enter<T>(
        tournament: &mut Tournament<T>,
        payment: Coin<T>,
        ctx: &TxContext,
    ) {
        let current_epoch = tx_context::epoch(ctx);
        assert!(current_epoch < tournament.start_epoch, 1);
        assert!(coin::value(&payment) == tournament.entry_fee, 2);
        
        let sender = tx_context::sender(ctx);
        assert!(!is_entrant(&tournament.entrants, sender), 3);
        
        vector::push_back(&mut tournament.entrants, sender);
        coin::join(&mut tournament.pool, payment);
    }

    public fun declare_result<T>(
        cap: OrganizerCap,
        tournament: Tournament<T>,
        first: address,
        second: address,
        third: address,
        ctx: &mut TxContext,
    ) {
        assert!(first != second && second != third && first != third, 4);
        assert!(is_entrant(&tournament.entrants, first), 5);
        assert!(is_entrant(&tournament.entrants, second), 5);
        assert!(is_entrant(&tournament.entrants, third), 5);
        
        let pool_value = coin::value(&tournament.pool);
        let first_amount = pool_value / 2;
        let second_amount = (pool_value * 30) / 100;
        let third_amount = (pool_value * 20) / 100;
        let remainder = pool_value - first_amount - second_amount - third_amount;
        let first_amount = first_amount + remainder;
        
        let Tournament { id, pool, entrants: _, .. } = tournament;
        let mut pool = pool;
        
        let first_coin = coin::split(&mut pool, first_amount, ctx);
        let second_coin = coin::split(&mut pool, second_amount, ctx);
        let third_coin = coin::split(&mut pool, third_amount, ctx);
        
        transfer::public_transfer(first_coin, first);
        transfer::public_transfer(second_coin, second);
        transfer::public_transfer(third_coin, third);
        
        coin::burn_for_testing(pool);
        object::delete(id);
        
        let OrganizerCap { id: cap_id, .. } = cap;
        object::delete(cap_id);
    }

    public fun cancel<T>(
        cap: OrganizerCap,
        tournament: Tournament<T>,
        ctx: &mut TxContext,
    ) {
        assert!(vector::length(&tournament.entrants) < 3, 6);
        
        let Tournament { id, pool, entrants, .. } = tournament;
        let mut pool = pool;
        
        let pool_value = coin::value(&pool);
        let per_entrant = pool_value / vector::length(&entrants);
        
        let mut i = 0;
        while (i < vector::length(&entrants)) {
            let entrant = *vector::borrow(&entrants, i);
            let refund = coin::split(&mut pool, per_entrant, ctx);
            transfer::public_transfer(refund, entrant);
            i = i + 1;
        };
        
        coin::burn_for_testing(pool);
        object::delete(id);
        
        let OrganizerCap { id: cap_id, .. } = cap;
        object::delete(cap_id);
    }

    fun is_entrant(entrants: &vector<address>, addr: address): bool {
        let mut i = 0;
        while (i < vector::length(entrants)) {
            if (*vector::borrow(entrants, i) == addr) {
                return true
            };
            i = i + 1;
        };
        false
    }

    public fun pool_amount<T>(tournament: &Tournament<T>): u64 {
        coin::value(&tournament.pool)
    }

    public fun entrant_count<T>(tournament: &Tournament<T>): u64 {
        vector::length(&tournament.entrants)
    }
}
