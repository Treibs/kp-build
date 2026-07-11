module balance_api_on_coin_red::till {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;

    public struct Till has key {
        id: UID,
        funds: Coin<SUI>,
    }

    // coin::put deposits into a Balance — a Coin-typed pool field
    // hands it the wrong receiver (see green: store Balance<SUI>)
    public fun pay_in(till: &mut Till, payment: Coin<SUI>) {
        coin::put(&mut till.funds, payment)
    }
}
