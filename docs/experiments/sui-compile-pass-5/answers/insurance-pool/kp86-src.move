module insurance::pool {
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};
    use sui::sui::SUI;
    use sui::event;

    public struct Pool has key {
        id: UID,
        reserves: Balance<SUI>,
        minimum_premium: u64,
        float_level: u64,
    }

    public struct AdjusterCap has key, store {
        id: UID,
    }

    public struct Policy has key, store {
        id: UID,
        holder: address,
        coverage: u64,
    }

    public struct PolicyBought has copy, drop {
        holder: address,
        coverage: u64,
        premium: u64,
    }

    public struct ClaimApproved has copy, drop {
        holder: address,
        payout: u64,
    }

    fun init(ctx: &mut TxContext) {
        let pool = Pool {
            id: object::new(ctx),
            reserves: balance::zero(),
            minimum_premium: 1_000_000_000,
            float_level: 100_000_000_000,
        };

        let adjuster_cap = AdjusterCap {
            id: object::new(ctx),
        };

        transfer::share_object(pool);
        transfer::public_transfer(adjuster_cap, ctx.sender());
    }

    public fun buy_policy(
        pool: &mut Pool,
        premium: Coin<SUI>,
        coverage: u64,
        ctx: &mut TxContext,
    ): Policy {
        let premium_value = coin::value(&premium);
        assert!(premium_value >= pool.minimum_premium, 1);

        balance::join(&mut pool.reserves, coin::into_balance(premium));

        let policy = Policy {
            id: object::new(ctx),
            holder: ctx.sender(),
            coverage,
        };

        event::emit(PolicyBought {
            holder: ctx.sender(),
            coverage,
            premium: premium_value,
        });

        policy
    }

    public fun approve_claim(
        _adjuster_cap: &AdjusterCap,
        pool: &mut Pool,
        policy: Policy,
        ctx: &mut TxContext,
    ) {
        let Policy { id, holder, coverage } = policy;
        object::delete(id);

        let available = balance::value(&pool.reserves);
        let payout = if (coverage <= available) {
            coverage
        } else {
            available
        };

        assert!(payout > 0, 2);

        let payout_balance = balance::split(&mut pool.reserves, payout);
        let payout_coin = coin::from_balance(payout_balance, ctx);

        transfer::public_transfer(payout_coin, holder);

        event::emit(ClaimApproved {
            holder,
            payout,
        });
    }

    public fun withdraw_reserves(
        _adjuster_cap: &AdjusterCap,
        pool: &mut Pool,
        amount: u64,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let available = balance::value(&pool.reserves);
        let excess = if (available > pool.float_level) {
            available - pool.float_level
        } else {
            0
        };

        assert!(amount <= excess, 3);

        let withdraw_balance = balance::split(&mut pool.reserves, amount);
        coin::from_balance(withdraw_balance, ctx)
    }
}
