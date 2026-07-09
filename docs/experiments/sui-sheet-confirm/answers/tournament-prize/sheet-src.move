module tournament::prize_pool {
    use sui::object::{Self, UID, ID};
    use sui::coin::{Coin, Self};
    use sui::transfer;
    use sui::table::{Table, Self as table_module};
    use sui::sui::SUI;
    use sui::clock::Clock;
    use std::vector;

    public struct Tournament has key {
        id: UID,
        entry_fee: u64,
        start_epoch: u64,
        pool: Coin<SUI>,
        entrants: Table<address, bool>,
        entrant_list: vector<address>,
    }

    public struct OrganizerCap has key, store {
        id: UID,
        tournament_id: ID,
    }

    public fun create_tournament(
        entry_fee: u64,
        start_epoch: u64,
        ctx: &mut TxContext,
    ): OrganizerCap {
        let tournament = Tournament {
            id: object::new(ctx),
            entry_fee,
            start_epoch,
            pool: coin::zero(ctx),
            entrants: table_module::new(ctx),
            entrant_list: vector[],
        };

        let tournament_id = object::id(&tournament);
        transfer::share_object(tournament);

        OrganizerCap {
            id: object::new(ctx),
            tournament_id,
        }
    }

    public fun enter(
        tournament: &mut Tournament,
        mut payment: Coin<SUI>,
        clock: &Clock,
        ctx: &mut TxContext,
    ) {
        let sender = ctx.sender();
        
        assert!(clock.timestamp_ms() < tournament.start_epoch, 1);
        assert!(!tournament.entrants.contains(sender), 2);
        assert!(coin::value(&payment) == tournament.entry_fee, 3);
        
        tournament.entrants.add(sender, true);
        vector::push_back(&mut tournament.entrant_list, sender);
        
        coin::join(&mut tournament.pool, payment);
    }

    public fun declare_result(
        cap: &OrganizerCap,
        mut tournament: Tournament,
        first: address,
        second: address,
        third: address,
        ctx: &mut TxContext,
    ) {
        assert!(cap.tournament_id == object::id(&tournament), 9);
        assert!(first != second && second != third && first != third, 4);
        assert!(tournament.entrants.contains(first), 5);
        assert!(tournament.entrants.contains(second), 6);
        assert!(tournament.entrants.contains(third), 7);
        
        let total_pool = coin::value(&tournament.pool);
        let first_payout = (total_pool * 50) / 100;
        let second_payout = (total_pool * 30) / 100;
        let third_payout = (total_pool * 20) / 100;
        let remainder = total_pool - first_payout - second_payout - third_payout;
        let first_payout = first_payout + remainder;
        
        let first_coin = coin::split(&mut tournament.pool, first_payout, ctx);
        let second_coin = coin::split(&mut tournament.pool, second_payout, ctx);
        
        transfer::public_transfer(first_coin, first);
        transfer::public_transfer(second_coin, second);
        
        let Tournament { id, entry_fee: _, start_epoch: _, pool, entrants, entrant_list: _ } = tournament;
        transfer::public_transfer(pool, third);
        
        object::delete(id);
        table_module::drop(entrants);
    }

    public fun cancel(
        cap: &OrganizerCap,
        mut tournament: Tournament,
        ctx: &mut TxContext,
    ) {
        assert!(cap.tournament_id == object::id(&tournament), 9);
        assert!(vector::length(&tournament.entrant_list) < 3, 8);
        
        let len = vector::length(&tournament.entrant_list);
        let mut i = 0;
        
        while (i < len) {
            let addr = *vector::borrow(&tournament.entrant_list, i);
            let refund = coin::split(&mut tournament.pool, tournament.entry_fee, ctx);
            transfer::public_transfer(refund, addr);
            i = i + 1;
        };
        
        let Tournament { id, entry_fee: _, start_epoch: _, pool, entrants, entrant_list: _ } = tournament;
        
        transfer::public_transfer(pool, ctx.sender());
        
        object::delete(id);
        table_module::drop(entrants);
    }

    public fun pool_amount(tournament: &Tournament): u64 {
        coin::value(&tournament.pool)
    }

    public fun entrant_count(tournament: &Tournament): u64 {
        vector::length(&tournament.entrant_list) as u64
    }
}
