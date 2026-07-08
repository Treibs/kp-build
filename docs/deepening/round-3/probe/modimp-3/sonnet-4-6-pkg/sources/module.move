module pool::tipjar {
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;

    public struct TipJar has key {
        id: UID,
        balance: Balance<SUI>,
    }

    public struct PerformerCap has key, store {
        id: UID,
    }

    public fun create(ctx: &mut TxContext) {
        let cap = PerformerCap { id: object::new(ctx) };
        transfer::public_transfer(cap, ctx.sender());

        let jar = TipJar {
            id: object::new(ctx),
            balance: balance::zero(),
        };
        transfer::share_object(jar);
    }

    public fun tip(jar: &mut TipJar, coin: Coin<SUI>) {
        jar.balance.join(coin::into_balance(coin));
    }

    public fun sweep(jar: &mut TipJar, _cap: &PerformerCap, ctx: &mut TxContext): Coin<SUI> {
        let amount = jar.balance.value();
        let bal = jar.balance.split(amount);
        coin::from_balance(bal, ctx)
    }

    public fun pooled_amount(jar: &TipJar): u64 {
        jar.balance.value()
    }
}
