module barn_dance::contest {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use std::option::{Self, Option};
    use std::vector;
    
    struct AdminCap has key {
        id: UID,
    }
    
    struct Couple has store, copy, drop {
        dancer1: address,
        dancer2: address,
    }
    
    struct Contest has key {
        id: UID,
        purse: Coin<SUI>,
        entry_fee: u64,
        prize_per_person: u64,
        couples: vector<Option<Couple>>,
        closed: bool,
        dancers_in_contest: vector<address>,
    }
    
    public fun create_contest(
        entry_fee: u64,
        prize_per_person: u64,
        ctx: &mut TxContext,
    ) {
        let id = object::new(ctx);
        let purse = coin::zero<SUI>(ctx);
        let contest = Contest {
            id,
            purse,
            entry_fee,
            prize_per_person,
            couples: vector::empty(),
            closed: false,
            dancers_in_contest: vector::empty(),
        };
        transfer::share_object(contest);
        
        let admin_cap = AdminCap {
            id: object::new(ctx),
        };
        transfer::transfer(admin_cap, tx_context::sender(ctx));
    }
    
    public fun enter_couple(
        contest: &mut Contest,
        dancer1: address,
        dancer2: address,
        payment: Coin<SUI>,
    ) {
        assert!(!contest.closed, 0);
        assert!(coin::value(&payment) == contest.entry_fee, 1);
        
        check_dancer_not_in_contest(contest, dancer1);
        check_dancer_not_in_contest(contest, dancer2);
        
        coin::join(&mut contest.purse, payment);
        
        let couple = Couple {
            dancer1,
            dancer2,
        };
        
        vector::push_back(&mut contest.couples, option::some(couple));
        vector::push_back(&mut contest.dancers_in_contest, dancer1);
        vector::push_back(&mut contest.dancers_in_contest, dancer2);
    }
    
    fun check_dancer_not_in_contest(contest: &Contest, dancer: address) {
        let len = vector::length(&contest.dancers_in_contest);
        let mut i = 0;
        while (i < len) {
            let d = *vector::borrow(&contest.dancers_in_contest, i);
            assert!(d != dancer, 2);
            i = i + 1;
        };
    }
    
    public fun eliminate_couple(
        contest: &mut Contest,
        _cap: &AdminCap,
        couple_index: u64,
    ) {
        let couples_remaining = count_standing_couples(contest);
        assert!(couples_remaining > 1, 3);
        
        if (couple_index < vector::length(&contest.couples)) {
            *vector::borrow_mut(&mut contest.couples, couple_index) = option::none();
        };
    }
    
    public fun close_contest(
        contest: &mut Contest,
        _cap: &AdminCap,
        ctx: &mut TxContext,
    ) {
        let couples_remaining = count_standing_couples(contest);
        assert!(couples_remaining == 1, 4);
        
        let prize_needed = contest.prize_per_person * 2;
        assert!(coin::value(&contest.purse) >= prize_needed, 5);
        
        let winner = find_winning_couple(contest);
        
        let prize1 = coin::split(&mut contest.purse, contest.prize_per_person, ctx);
        let prize2 = coin::split(&mut contest.purse, contest.prize_per_person, ctx);
        
        transfer::public_transfer(prize1, winner.dancer1);
        transfer::public_transfer(prize2, winner.dancer2);
        
        contest.closed = true;
    }
    
    fun find_winning_couple(contest: &Contest): Couple {
        let len = vector::length(&contest.couples);
        let mut i = 0;
        while (i < len) {
            let couple_opt = vector::borrow(&contest.couples, i);
            if (option::is_some(couple_opt)) {
                return *option::borrow(couple_opt)
            };
            i = i + 1;
        };
        abort 6
    }
    
    public fun top_up_purse(
        contest: &mut Contest,
        payment: Coin<SUI>,
    ) {
        coin::join(&mut contest.purse, payment);
    }
    
    public fun view_couples(contest: &Contest): u64 {
        count_standing_couples(contest)
    }
    
    public fun view_purse_balance(contest: &Contest): u64 {
        coin::value(&contest.purse)
    }
    
    fun count_standing_couples(contest: &Contest): u64 {
        let mut count = 0;
        let len = vector::length(&contest.couples);
        let mut i = 0;
        while (i < len) {
            if (option::is_some(vector::borrow(&contest.couples, i))) {
                count = count + 1;
            };
            i = i + 1;
        };
        count
    }
}
