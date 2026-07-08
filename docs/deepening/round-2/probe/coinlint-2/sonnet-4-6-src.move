module vend::machine;

use sui::coin::{Self, Coin};
use sui::balance::{Self, Balance};
use sui::sui::SUI;

public struct VendingMachine has key {
    id: UID,
    price: u64,
    proceeds: Balance<SUI>,
}

public struct Widget has key {
    id: UID,
}

public struct MachineCap has key, store {
    id: UID,
}

public fun create(price: u64, ctx: &mut TxContext) {
    let machine = VendingMachine {
        id: object::new(ctx),
        price,
        proceeds: balance::zero(),
    };
    let cap = MachineCap { id: object::new(ctx) };
    transfer::transfer(cap, ctx.sender());
    transfer::share_object(machine);
}

public fun buy(machine: &mut VendingMachine, mut payment: Coin<SUI>, ctx: &mut TxContext) {
    assert!(payment.value() >= machine.price);
    let price_coin = payment.split(machine.price, ctx);
    balance::join(&mut machine.proceeds, coin::into_balance(price_coin));
    transfer::transfer(Widget { id: object::new(ctx) }, ctx.sender());
    if (payment.value() > 0) {
        transfer::public_transfer(payment, ctx.sender());
    } else {
        coin::destroy_zero(payment);
    };
}

public fun collect(machine: &mut VendingMachine, _cap: &MachineCap, ctx: &mut TxContext) {
    let amount = balance::value(&machine.proceeds);
    let proceeds = coin::take(&mut machine.proceeds, amount, ctx);
    transfer::public_transfer(proceeds, ctx.sender());
}
