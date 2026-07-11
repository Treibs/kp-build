module balance_api_on_coin_green::till {
    use sui::balance::Balance;
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;

    // the accumulating pool is a Balance; Coin is the boundary type —
    // put deposits a Coin into the Balance, take mints a Coin back out
    public struct Till has key {
        id: UID,
        funds: Balance<SUI>,
    }

    public fun pay_in(till: &mut Till, payment: Coin<SUI>) {
        coin::put(&mut till.funds, payment)
    }

    public fun pay_out(till: &mut Till, amount: u64, ctx: &mut TxContext): Coin<SUI> {
        coin::take(&mut till.funds, amount, ctx)
    }
}
