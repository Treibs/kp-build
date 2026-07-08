module pot::savings {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};

    public struct SavingsPot has key {
        id: UID,
        balance: Balance<SUI>,
    }

    public fun create(ctx: &mut TxContext) {
        let pot = SavingsPot {
            id: object::new(ctx),
            balance: balance::zero(),
        };
        transfer::transfer(pot, ctx.sender());
    }

    public fun deposit(pot: &mut SavingsPot, coin: Coin<SUI>) {
        coin::put(&mut pot.balance, coin);
    }

    public fun withdraw_all(pot: &mut SavingsPot, ctx: &mut TxContext) {
        let amount = balance::value(&pot.balance);
        let coin = coin::take(&mut pot.balance, amount, ctx);
        transfer::public_transfer(coin, ctx.sender());
    }
}
