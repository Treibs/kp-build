module insurance::pool {
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::object::{Self, UID, ID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::event;

    struct InsurancePool has key {
        id: UID,
        reserves: Balance<SUI>,
        min_premium: u64,
        float: u64,
    }

    struct AdjusterCap has key {
        id: UID,
        pool_id: ID,
    }

    struct Policy has key {
        id: UID,
        holder: address,
        coverage: u64,
        pool_id: ID,
    }

    struct PoolCreated has copy, drop {
        pool_id: ID,
    }

    struct PolicyPurchased has copy, drop {
        policy_id: ID,
        holder: address,
        coverage: u64,
    }

    struct ClaimApproved has copy, drop {
        policy_id: ID,
        payout: u64,
    }

    struct ReservesWithdrawn has copy, drop {
        amount: u64,
    }

    public fun create_pool(min_premium: u64, float: u64, ctx: &mut TxContext) {
        let pool_id = object::new(ctx);
        let pool_id_val = object::uid_to_inner(&pool_id);
        
        let pool = InsurancePool {
            id: pool_id,
            reserves: balance::zero(),
            min_premium,
            float,
        };

        let adjuster_cap = AdjusterCap {
            id: object::new(ctx),
            pool_id: pool_id_val,
        };

        event::emit(PoolCreated { pool_id: pool_id_val });

        transfer::share_object(pool);
        transfer::transfer(adjuster_cap, tx_context::sender(ctx));
    }

    public fun buy_policy(
        pool: &mut InsurancePool,
        premium: Coin<SUI>,
        coverage: u64,
        ctx: &mut TxContext,
    ): Policy {
        let premium_amount = coin::value(&premium);
        assert!(premium_amount >= pool.min_premium, 1);

        balance::join(&mut pool.reserves, coin::into_balance(premium));

        let holder = tx_context::sender(ctx);
        let policy = Policy {
            id: object::new(ctx),
            holder,
            coverage,
            pool_id: object::uid_to_inner(&pool.id),
        };

        event::emit(PolicyPurchased {
            policy_id: object::uid_to_inner(&policy.id),
            holder,
            coverage,
        });

        policy
    }

    public fun approve_claim(
        cap: &AdjusterCap,
        pool: &mut InsurancePool,
        policy: Policy,
        payout_amount: u64,
        ctx: &mut TxContext,
    ) {
        assert!(cap.pool_id == object::uid_to_inner(&pool.id), 5);
        assert!(policy.pool_id == object::uid_to_inner(&pool.id), 6);
        assert!(payout_amount <= policy.coverage, 2);
        assert!(balance::value(&pool.reserves) >= payout_amount, 3);

        let Policy { id, holder, coverage: _, pool_id: _ } = policy;
        let policy_id = object::uid_to_inner(&id);
        object::delete(id);

        let payout = balance::split(&mut pool.reserves, payout_amount);
        
        event::emit(ClaimApproved {
            policy_id,
            payout: payout_amount,
        });

        transfer::public_transfer(coin::from_balance(payout, ctx), holder);
    }

    public fun withdraw_reserves(
        pool: &mut InsurancePool,
        amount: u64,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let current_reserves = balance::value(&pool.reserves);
        assert!(amount + pool.float <= current_reserves, 4);

        let withdrawn = balance::split(&mut pool.reserves, amount);
        
        event::emit(ReservesWithdrawn { amount });

        coin::from_balance(withdrawn, ctx)
    }

    public fun pool_reserves(pool: &InsurancePool): u64 {
        balance::value(&pool.reserves)
    }

    public fun pool_float(pool: &InsurancePool): u64 {
        pool.float
    }

    public fun pool_min_premium(pool: &InsurancePool): u64 {
        pool.min_premium
    }

    public fun policy_holder(policy: &Policy): address {
        policy.holder
    }

    public fun policy_coverage(policy: &Policy): u64 {
        policy.coverage
    }
}
