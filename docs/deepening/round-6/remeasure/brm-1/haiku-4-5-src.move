module rain_insurance::policy {
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;
    use sui::transfer;
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};
    use sui::dynamic_field;
    use sui::sui::SUI;

    public struct Policy has key, store {
        id: UID,
        epoch: u64,
        premium_amount: u64,
    }

    public struct Pool has key {
        id: UID,
        balance: Balance<SUI>,
    }

    public struct OracleCap has key, store {
        id: UID,
    }

    public struct POLICY has drop {}

    fun init(witness: POLICY, ctx: &mut TxContext) {
        let pool = Pool {
            id: object::new(ctx),
            balance: balance::zero(),
        };
        transfer::share_object(pool);

        let oracle_cap = OracleCap {
            id: object::new(ctx),
        };
        transfer::transfer(oracle_cap, ctx.sender());
    }

    public fun buy_policy(
        pool: &mut Pool,
        premium: Coin<SUI>,
        epoch: u64,
        ctx: &mut TxContext,
    ): Policy {
        let amount = coin::value(&premium);
        coin::put(&mut pool.balance, premium);

        Policy {
            id: object::new(ctx),
            epoch,
            premium_amount: amount,
        }
    }

    public fun mark_epoch(
        _cap: &OracleCap,
        pool: &mut Pool,
        epoch: u64,
        is_rainy: bool,
    ) {
        dynamic_field::add(&mut pool.id, epoch, is_rainy);
    }

    public fun settle_policy(
        policy: Policy,
        pool: &mut Pool,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let Policy { id, epoch, premium_amount } = policy;
        object::delete(id);

        let is_rainy = *dynamic_field::borrow<u64, bool>(&pool.id, epoch);

        let payout_amount = if (is_rainy) {
            premium_amount * 2
        } else {
            0
        };

        coin::take(&mut pool.balance, payout_amount, ctx)
    }
}
