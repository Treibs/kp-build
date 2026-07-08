module park::meter {
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};
    use sui::sui::SUI;

    public struct Meter has key {
        id: UID,
        price_per_hour: u64,
        collected: Balance<SUI>,
    }

    public struct Permit has key {
        id: UID,
        hours: u64,
        epoch: u64,
    }

    public struct CityCap has key, store {
        id: UID,
    }

    public fun create(price_per_hour: u64, ctx: &mut TxContext) {
        let meter = Meter {
            id: object::new(ctx),
            price_per_hour,
            collected: balance::zero(),
        };
        transfer::share_object(meter);
        let cap = CityCap { id: object::new(ctx) };
        transfer::public_transfer(cap, ctx.sender());
    }

    public fun park(meter: &mut Meter, mut payment: Coin<SUI>, hours: u64, ctx: &mut TxContext) {
        let owed = meter.price_per_hour * hours;
        assert!(payment.value() >= owed);
        let owed_coin = payment.split(owed, ctx);
        balance::join(&mut meter.collected, owed_coin.into_balance());
        if (payment.value() > 0) {
            transfer::public_transfer(payment, ctx.sender());
        } else {
            coin::destroy_zero(payment);
        };
        let permit = Permit {
            id: object::new(ctx),
            hours,
            epoch: ctx.epoch(),
        };
        transfer::transfer(permit, ctx.sender());
    }

    public fun sweep(_cap: &CityCap, meter: &mut Meter, ctx: &mut TxContext) {
        let amount = meter.collected.value();
        let swept = meter.collected.split(amount);
        transfer::public_transfer(coin::from_balance(swept, ctx), ctx.sender());
    }
}
