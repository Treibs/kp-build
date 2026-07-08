module swap_pool::pool {
    use sui::coin::{Self, Coin};
    use sui::transfer;
    use sui::object;
    use sui::tx_context::TxContext;

    public struct Pool<phantom A, phantom B> has key {
        id: UID,
        fee_bps: u64,
        coins_a: Coin<A>,
        coins_b: Coin<B>,
    }

    public struct PoolCapability has key, store {
        id: UID,
        pool_id: object::ID,
    }

    public fun create_pool<A, B>(
        coin_a: Coin<A>,
        coin_b: Coin<B>,
        fee_bps: u64,
        ctx: &mut TxContext,
    ): (Pool<A, B>, PoolCapability) {
        let pool = Pool<A, B> {
            id: object::new(ctx),
            fee_bps,
            coins_a: coin_a,
            coins_b: coin_b,
        };

        let cap = PoolCapability {
            id: object::new(ctx),
            pool_id: object::id(&pool),
        };

        (pool, cap)
    }

    public fun swap<A, B>(
        pool: &mut Pool<A, B>,
        coin_in: Coin<A>,
        ctx: &mut TxContext,
    ): Coin<B> {
        let amount_in = coin::value(&coin_in);
        let amount_in_with_fee = amount_in * (10000 - pool.fee_bps) / 10000;
        
        let reserve_a = coin::value(&pool.coins_a);
        let reserve_b = coin::value(&pool.coins_b);
        
        coin::join(&mut pool.coins_a, coin_in);
        
        let numerator = (amount_in_with_fee as u128) * (reserve_b as u128);
        let denominator = (reserve_a as u128) + (amount_in_with_fee as u128);
        let output = numerator / denominator;
        
        assert!(output > 0, 0);
        
        coin::split(&mut pool.coins_b, (output as u64), ctx)
    }

    public fun add_liquidity<A, B>(
        cap: &PoolCapability,
        pool: &mut Pool<A, B>,
        coin_a: Coin<A>,
        coin_b: Coin<B>,
    ) {
        assert!(cap.pool_id == object::id(pool), 1);
        coin::join(&mut pool.coins_a, coin_a);
        coin::join(&mut pool.coins_b, coin_b);
    }

    public fun close_pool<A, B>(
        cap: PoolCapability,
        pool: Pool<A, B>,
    ): (Coin<A>, Coin<B>) {
        assert!(cap.pool_id == object::id(&pool), 1);
        
        let PoolCapability { id: cap_id, pool_id: _ } = cap;
        object::delete(cap_id);
        
        let Pool { id: pool_id, fee_bps: _, coins_a, coins_b } = pool;
        object::delete(pool_id);
        
        (coins_a, coins_b)
    }

    public fun get_reserves<A, B>(pool: &Pool<A, B>): (u64, u64) {
        (coin::value(&pool.coins_a), coin::value(&pool.coins_b))
    }
}
