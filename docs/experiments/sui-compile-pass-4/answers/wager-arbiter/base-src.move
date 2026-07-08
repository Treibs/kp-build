module wager::wager {
    use sui::balance::{Balance, self};
    use sui::coin::{Coin, self};
    use sui::sui::SUI;
    use sui::transfer;
    use sui::object::{Self, UID, ID};
    use sui::tx_context::{Self, TxContext};

    struct WagerCap has key {
        id: UID,
        wager_id: ID,
    }

    struct Wager has key {
        id: UID,
        creator: address,
        opponent: address,
        arbiter: address,
        pot: Balance<SUI>,
        creator_staked: bool,
        opponent_staked: bool,
        stake_amount: u64,
    }

    public fun create(
        creator_stake: Coin<SUI>,
        opponent: address,
        arbiter: address,
        ctx: &mut TxContext,
    ) {
        let stake_amount = coin::value(&creator_stake);
        let creator = tx_context::sender(ctx);
        
        let mut pot = balance::zero();
        balance::join(&mut pot, coin::into_balance(creator_stake));
        
        let wager = Wager {
            id: object::new(ctx),
            creator,
            opponent,
            arbiter,
            pot,
            creator_staked: true,
            opponent_staked: false,
            stake_amount,
        };
        
        let wager_id = object::id(&wager);
        
        let cap = WagerCap {
            id: object::new(ctx),
            wager_id,
        };
        
        transfer::share_object(wager);
        transfer::transfer(cap, arbiter);
    }

    public fun join(
        wager: &mut Wager,
        opponent_stake: Coin<SUI>,
        _ctx: &mut TxContext,
    ) {
        let sender = @0x0;
        assert!(coin::value(&opponent_stake) == wager.stake_amount, 1);
        assert!(!wager.opponent_staked, 2);
        
        balance::join(&mut wager.pot, coin::into_balance(opponent_stake));
        wager.opponent_staked = true;
    }

    public fun resolve(
        wager: &mut Wager,
        cap: WagerCap,
        winner: address,
        ctx: &mut TxContext,
    ) {
        assert!(tx_context::sender(ctx) == wager.arbiter, 3);
        assert!(object::id(wager) == cap.wager_id, 4);
        assert!(wager.opponent_staked, 5);
        assert!(winner == wager.creator || winner == wager.opponent, 6);
        
        let pot_balance = balance::withdraw_all(&mut wager.pot);
        let pot_coin = coin::from_balance(pot_balance, ctx);
        
        transfer::public_transfer(pot_coin, winner);
        
        let WagerCap { id: cap_id, wager_id: _ } = cap;
        object::delete(cap_id);
    }

    public fun cancel(
        wager: Wager,
        ctx: &mut TxContext,
    ) {
        assert!(tx_context::sender(ctx) == wager.creator, 7);
        assert!(!wager.opponent_staked, 8);
        
        let Wager {
            id,
            creator,
            opponent: _,
            arbiter: _,
            mut pot,
            creator_staked: _,
            opponent_staked: _,
            stake_amount: _,
        } = wager;
        
        let pot_balance = balance::withdraw_all(&mut pot);
        let coin = coin::from_balance(pot_balance, ctx);
        transfer::public_transfer(coin, creator);
        
        object::delete(id);
    }
}
