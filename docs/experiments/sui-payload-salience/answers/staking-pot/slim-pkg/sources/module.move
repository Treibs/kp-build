module staking::pool {
    use sui::coin::{Coin, Self};
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;
    use sui::transfer;
    use sui::balance::{Balance, Self};
    use sui::clock::Clock;
    
    public struct PoolOwnerCap has key, store {
        id: UID,
    }
    
    public struct RewardPool has key {
        id: UID,
        reward_reservoir: Balance<SUI>,
        per_epoch_rate_bps: u64,
    }
    
    public struct StakePosition has key {
        id: UID,
        staked_coin: Coin<SUI>,
        start_epoch: u64,
    }
    
    fun init(ctx: &mut TxContext) {
        let cap = PoolOwnerCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, ctx.sender());
    }
    
    public fun create_pool(
        _cap: &PoolOwnerCap,
        reward_fund: Coin<SUI>,
        per_epoch_rate_bps: u64,
        ctx: &mut TxContext,
    ) {
        let pool = RewardPool {
            id: object::new(ctx),
            reward_reservoir: coin::into_balance(reward_fund),
            per_epoch_rate_bps,
        };
        transfer::share_object(pool);
    }
    
    public fun stake(
        staked_coin: Coin<SUI>,
        clock: &Clock,
        ctx: &mut TxContext,
    ): StakePosition {
        let epoch = clock.timestamp_ms() / (24 * 60 * 60 * 1000);
        
        StakePosition {
            id: object::new(ctx),
            staked_coin,
            start_epoch: epoch,
        }
    }
    
    public fun unstake(
        pool: &mut RewardPool,
        position: StakePosition,
        clock: &Clock,
        ctx: &mut TxContext,
    ) {
        let StakePosition { id, staked_coin, start_epoch } = position;
        object::delete(id);
        
        let principal = coin::value(&staked_coin);
        let current_epoch = clock.timestamp_ms() / (24 * 60 * 60 * 1000);
        let epochs_elapsed = current_epoch - start_epoch;
        
        let reward = (principal * pool.per_epoch_rate_bps * epochs_elapsed) / 10_000;
        
        let available = balance::value(&pool.reward_reservoir);
        assert!(available >= reward, 0);
        
        let reward_balance = balance::split(&mut pool.reward_reservoir, reward);
        let reward_coin = coin::from_balance(reward_balance, ctx);
        
        let mut payout = staked_coin;
        coin::join(&mut payout, reward_coin);
        
        transfer::public_transfer(payout, ctx.sender());
    }
    
    public fun top_up(
        _cap: &PoolOwnerCap,
        pool: &mut RewardPool,
        top_up_coin: Coin<SUI>,
    ) {
        let balance = coin::into_balance(top_up_coin);
        balance::join(&mut pool.reward_reservoir, balance);
    }
    
    public fun reservoir_balance(pool: &RewardPool): u64 {
        balance::value(&pool.reward_reservoir)
    }
}
