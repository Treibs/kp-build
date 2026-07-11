module barn_dance::contest {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};
    use sui::sui::SUI;
    use sui::table::{Self, Table};
    use std::vector;

    public struct Contest has key {
        id: UID,
        entry_fee: u64,
        prize: u64,
        purse: Balance<SUI>,
        couples: vector<Couple>,
        dancers: Table<address, bool>,
        closed: bool,
    }

    public struct Couple has copy, drop, store {
        dancer1: address,
        dancer2: address,
    }

    public struct Caller has key, store {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        let caller = Caller {
            id: object::new(ctx),
        };
        transfer::transfer(caller, tx_context::sender(ctx));
    }

    public fun create(
        entry_fee: u64,
        prize: u64,
        ctx: &mut TxContext,
    ): Contest {
        Contest {
            id: object::new(ctx),
            entry_fee,
            prize,
            purse: balance::zero(),
            couples: vector[],
            dancers: table::new(ctx),
            closed: false,
        }
    }

    public fun enter(
        contest: &mut Contest,
        dancer1: address,
        dancer2: address,
        payment: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let amount = coin::value(&payment);
        assert!(amount == contest.entry_fee, 0);
        assert!(!contest.closed, 1);
        assert!(dancer1 != dancer2, 2);
        assert!(!table::contains(&contest.dancers, dancer1), 3);
        assert!(!table::contains(&contest.dancers, dancer2), 4);

        table::add(&mut contest.dancers, dancer1, true);
        table::add(&mut contest.dancers, dancer2, true);

        let couple = Couple { dancer1, dancer2 };
        vector::push_back(&mut contest.couples, couple);

        let balance = coin::into_balance(payment);
        balance::join(&mut contest.purse, balance);
    }

    public fun eliminate(
        contest: &mut Contest,
        index: u64,
        _cap: &Caller,
    ) {
        let num_couples = vector::length(&contest.couples);
        assert!(num_couples > 1, 5);
        assert!(index < num_couples, 6);

        let couple = vector::swap_remove(&mut contest.couples, index);
        let _ = table::remove(&mut contest.dancers, couple.dancer1);
        let _ = table::remove(&mut contest.dancers, couple.dancer2);
    }

    public fun close(
        contest: &mut Contest,
        _cap: &Caller,
        ctx: &mut TxContext,
    ) {
        let num_couples = vector::length(&contest.couples);
        assert!(num_couples == 1, 7);

        let couple = vector::pop_back(&mut contest.couples);
        let prize_amount = contest.prize;
        assert!(balance::value(&contest.purse) >= prize_amount * 2, 8);

        let payment1 = coin::from_balance(
            balance::split(&mut contest.purse, prize_amount),
            ctx,
        );
        let payment2 = coin::from_balance(
            balance::split(&mut contest.purse, prize_amount),
            ctx,
        );

        transfer::public_transfer(payment1, couple.dancer1);
        transfer::public_transfer(payment2, couple.dancer2);

        let _ = table::remove(&mut contest.dancers, couple.dancer1);
        let _ = table::remove(&mut contest.dancers, couple.dancer2);

        contest.closed = true;
    }

    public fun sponsor_topup(
        contest: &mut Contest,
        payment: Coin<SUI>,
    ) {
        let balance = coin::into_balance(payment);
        balance::join(&mut contest.purse, balance);
    }

    public fun couples_standing(contest: &Contest): vector<Couple> {
        let mut result = vector[];
        let mut i = 0;
        while (i < vector::length(&contest.couples)) {
            vector::push_back(&mut result, *vector::borrow(&contest.couples, i));
            i = i + 1;
        };
        result
    }

    public fun purse_balance(contest: &Contest): u64 {
        balance::value(&contest.purse)
    }
}
