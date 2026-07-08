module wager::wager {
    use std::option::{Self, Option};
    use sui::coin::Coin;
    use sui::sui::SUI;

    public struct Wager has key, store {
        id: UID,
        creator: address,
        opponent: address,
        arbiter: address,
        stake_amount: u64,
        pot: Option<Coin<SUI>>,
        resolved: bool,
    }

    public struct ArbiterCapability has key, store {
        id: UID,
    }

    public fun create_wager(
        stake: Coin<SUI>,
        opponent: address,
        arbiter: address,
        ctx: &mut TxContext,
    ) {
        assert!(stake.value() > 0);
        
        let wager = Wager {
            id: object::new(ctx),
            creator: ctx.sender(),
            opponent,
            arbiter,
            stake_amount: stake.value(),
            pot: option::some(stake),
            resolved: false,
        };
        
        transfer::share_object(wager);
        
        let cap = ArbiterCapability {
            id: object::new(ctx),
        };
        
        transfer::transfer(cap, arbiter);
    }

    public fun join_wager(
        wager: &mut Wager,
        stake: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        assert!(!wager.resolved, 1);
        assert!(ctx.sender() == wager.opponent, 2);
        assert!(stake.value() == wager.stake_amount, 3);
        assert!(option::is_some(&wager.pot), 4);
        
        let mut pot = option::extract(&mut wager.pot);
        pot.join(stake);
        option::fill(&mut wager.pot, pot);
    }

    public fun resolve_wager(
        wager: &mut Wager,
        winner: address,
        _cap: &ArbiterCapability,
    ) {
        assert!(!wager.resolved, 5);
        assert!(option::is_some(&wager.pot), 6);
        
        let pot = option::extract(&mut wager.pot);
        transfer::public_transfer(pot, winner);
        wager.resolved = true;
    }

    public fun cancel_wager(
        wager: &mut Wager,
        ctx: &mut TxContext,
    ) {
        assert!(!wager.resolved, 7);
        assert!(ctx.sender() == wager.creator, 8);
        assert!(option::is_some(&wager.pot), 9);
        
        let pot = option::extract(&mut wager.pot);
        transfer::public_transfer(pot, wager.creator);
        wager.resolved = true;
    }
}
