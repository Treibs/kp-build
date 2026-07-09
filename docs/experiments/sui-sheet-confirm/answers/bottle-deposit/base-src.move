module bottle_deposit::scheme {
    use sui::object::{Self, UID, ID};
    use sui::transfer;
    use sui::tx_context::TxContext;
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};
    use sui::event;

    public struct BottleSold has copy, drop {
        bottle_id: ID,
        scheme_id: ID,
    }

    public struct BottleReturned has copy, drop {
        bottle_id: ID,
        scheme_id: ID,
    }

    public struct ReservoirToppedUp has copy, drop {
        scheme_id: ID,
        amount: u64,
    }

    public struct ReservoirWithdrawn has copy, drop {
        scheme_id: ID,
        amount: u64,
    }

    public struct DepositScheme has key {
        id: UID,
        deposit_amount: u64,
        reservoir: Balance<SUI>,
        sold_count: u64,
        returned_count: u64,
    }

    public struct DistributorCap has key {
        id: UID,
        scheme_id: ID,
    }

    public struct Bottle has key {
        id: UID,
        scheme_id: ID,
    }

    public fun create_scheme(deposit_amount: u64, ctx: &mut TxContext) {
        let scheme = DepositScheme {
            id: object::new(ctx),
            deposit_amount,
            reservoir: balance::zero(),
            sold_count: 0,
            returned_count: 0,
        };
        
        let scheme_id = object::uid_to_inner(&scheme.id);
        
        let cap = DistributorCap {
            id: object::new(ctx),
            scheme_id,
        };

        transfer::share_object(scheme);
        transfer::transfer(cap, tx_context::sender(ctx));
    }

    public fun sell_bottle(
        scheme: &mut DepositScheme,
        cap: &DistributorCap,
        payment: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let scheme_id = object::uid_to_inner(&scheme.id);
        assert!(cap.scheme_id == scheme_id, 0);
        assert!(coin::value(&payment) == scheme.deposit_amount, 1);

        balance::join(&mut scheme.reservoir, coin::into_balance(payment));
        scheme.sold_count = scheme.sold_count + 1;

        let bottle = Bottle {
            id: object::new(ctx),
            scheme_id,
        };

        let bottle_id = object::uid_to_inner(&bottle.id);
        transfer::transfer(bottle, tx_context::sender(ctx));

        event::emit(BottleSold {
            bottle_id,
            scheme_id,
        });
    }

    public fun return_bottle(
        scheme: &mut DepositScheme,
        bottle: Bottle,
        ctx: &mut TxContext,
    ) {
        let scheme_id = object::uid_to_inner(&scheme.id);
        assert!(bottle.scheme_id == scheme_id, 2);
        assert!(balance::value(&scheme.reservoir) >= scheme.deposit_amount, 3);
        
        let refund_balance = balance::split(&mut scheme.reservoir, scheme.deposit_amount);
        transfer::transfer(coin::from_balance(refund_balance, ctx), tx_context::sender(ctx));
        
        scheme.returned_count = scheme.returned_count + 1;

        let Bottle { id, scheme_id: _ } = bottle;
        let bottle_id = object::uid_to_inner(&id);
        object::delete(id);

        event::emit(BottleReturned {
            bottle_id,
            scheme_id,
        });
    }

    public fun top_up_reservoir(
        scheme: &mut DepositScheme,
        cap: &DistributorCap,
        deposit: Coin<SUI>,
    ) {
        let scheme_id = object::uid_to_inner(&scheme.id);
        assert!(cap.scheme_id == scheme_id, 4);

        let amount = coin::value(&deposit);
        balance::join(&mut scheme.reservoir, coin::into_balance(deposit));

        event::emit(ReservoirToppedUp {
            scheme_id,
            amount,
        });
    }

    public fun withdraw_from_reservoir(
        scheme: &mut DepositScheme,
        cap: &DistributorCap,
        amount: u64,
        ctx: &mut TxContext,
    ) {
        let scheme_id = object::uid_to_inner(&scheme.id);
        assert!(cap.scheme_id == scheme_id, 5);

        let outstanding = scheme.sold_count - scheme.returned_count;
        let liability = outstanding * scheme.deposit_amount;
        let available = balance::value(&scheme.reservoir) - liability;

        assert!(amount <= available, 6);

        let withdrawal_balance = balance::split(&mut scheme.reservoir, amount);
        transfer::transfer(coin::from_balance(withdrawal_balance, ctx), tx_context::sender(ctx));

        event::emit(ReservoirWithdrawn {
            scheme_id,
            amount,
        });
    }

    public fun get_outstanding_count(scheme: &DepositScheme): u64 {
        scheme.sold_count - scheme.returned_count
    }

    public fun get_reservoir_balance(scheme: &DepositScheme): u64 {
        balance::value(&scheme.reservoir)
    }

    public fun get_deposit_amount(scheme: &DepositScheme): u64 {
        scheme.deposit_amount
    }

    public fun get_returned_count(scheme: &DepositScheme): u64 {
        scheme.returned_count
    }

    public fun get_sold_count(scheme: &DepositScheme): u64 {
        scheme.sold_count
    }
}
