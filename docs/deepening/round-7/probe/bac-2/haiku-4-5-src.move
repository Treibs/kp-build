module dunk::tank {
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;

    public struct DunkTank has key {
        id: UID,
        pool: Balance<SUI>,
        throw_price: u64,
        prize_amount: u64,
        throws: u64,
        owner: address,
    }

    public struct AdminCap has key, store {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        let tank = DunkTank {
            id: object::new(ctx),
            pool: balance::zero(),
            throw_price: 1_000_000,
            prize_amount: 10_000_000,
            throws: 0,
            owner: tx_context::sender(ctx),
        };
        transfer::share_object(tank);

        let cap = AdminCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, tx_context::sender(ctx));
    }

    public fun play(
        tank: &mut DunkTank,
        payment: Coin<SUI>,
    ) {
        let amount = coin::value(&payment);
        assert!(amount >= tank.throw_price, 0);
        
        balance::join(&mut tank.pool, coin::into_balance(payment));
        tank.throws = tank.throws + 1;
    }

    public fun record_hit(
        _cap: &AdminCap,
        tank: &mut DunkTank,
        thrower: address,
        ctx: &mut TxContext,
    ) {
        assert!(balance::value(&tank.pool) >= tank.prize_amount, 1);
        
        let payout = coin::from_balance(
            balance::split(&mut tank.pool, tank.prize_amount),
            ctx,
        );
        transfer::public_transfer(payout, thrower);
    }

    public fun top_up_pool(
        _cap: &AdminCap,
        tank: &mut DunkTank,
        payment: Coin<SUI>,
    ) {
        balance::join(&mut tank.pool, coin::into_balance(payment));
    }

    public fun set_prize_amount(
        _cap: &AdminCap,
        tank: &mut DunkTank,
        new_amount: u64,
    ) {
        tank.prize_amount = new_amount;
    }

    public fun pool_balance(tank: &DunkTank): u64 {
        balance::value(&tank.pool)
    }

    public fun throw_count(tank: &DunkTank): u64 {
        tank.throws
    }

    public fun throw_price(tank: &DunkTank): u64 {
        tank.throw_price
    }

    public fun prize_amount(tank: &DunkTank): u64 {
        tank.prize_amount
    }
}
