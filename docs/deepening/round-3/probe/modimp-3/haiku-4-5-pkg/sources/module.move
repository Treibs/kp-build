module pool::tipjar {
    use sui::balance::{Balance, join, split, value, zero};
    use sui::coin::{Coin, into_balance, from_balance};
    use sui::sui::SUI;

    public struct TipJar has key {
        id: UID,
        balance: Balance<SUI>,
    }

    public struct PerformerCap has key, store {
        id: UID,
    }

    public fun create(ctx: &mut TxContext): PerformerCap {
        let jar = TipJar {
            id: object::new(ctx),
            balance: zero(),
        };
        transfer::share_object(jar);
        
        PerformerCap {
            id: object::new(ctx),
        }
    }

    public fun tip(jar: &mut TipJar, coin: Coin<SUI>) {
        join(&mut jar.balance, into_balance(coin));
    }

    public fun sweep(_cap: &PerformerCap, jar: &mut TipJar, ctx: &mut TxContext): Coin<SUI> {
        let amount = value(&jar.balance);
        let extracted = split(&mut jar.balance, amount);
        from_balance(extracted, ctx)
    }

    public fun get_balance(jar: &TipJar): u64 {
        value(&jar.balance)
    }
}
