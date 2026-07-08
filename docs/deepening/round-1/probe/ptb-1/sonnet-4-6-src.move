module basket::basket;

use sui::balance::{Self, Balance};
use sui::coin::Coin;
use sui::sui::SUI;

public struct Basket has key {
    id: UID,
    balance: Balance<SUI>,
}

public fun new(ctx: &mut TxContext): Basket {
    Basket {
        id: object::new(ctx),
        balance: balance::zero(),
    }
}

entry fun deposit(basket: &mut Basket, coin: Coin<SUI>) {
    basket.balance.join(coin.into_balance());
}

public fun value(basket: &Basket): u64 {
    basket.balance.value()
}
