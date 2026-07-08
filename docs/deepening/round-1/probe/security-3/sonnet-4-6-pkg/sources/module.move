module bank::bank {
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::table::{Self, Table};

    const EInsufficientFunds: u64 = 0;

    public struct Bank has key {
        id: UID,
        pool: Balance<SUI>,
        balances: Table<address, u64>,
    }

    fun init(ctx: &mut TxContext) {
        transfer::share_object(Bank {
            id: object::new(ctx),
            pool: balance::zero(),
            balances: table::new(ctx),
        });
    }

    public fun deposit(bank: &mut Bank, coin: Coin<SUI>, ctx: &mut TxContext) {
        let sender = ctx.sender();
        let amount = coin.value();
        balance::join(&mut bank.pool, coin.into_balance());
        if (table::contains(&bank.balances, sender)) {
            let bal = table::borrow_mut(&mut bank.balances, sender);
            *bal = *bal + amount;
        } else {
            table::add(&mut bank.balances, sender, amount);
        }
    }

    entry fun withdraw(bank: &mut Bank, amount: u64, ctx: &mut TxContext) {
        let sender = ctx.sender();
        assert!(table::contains(&bank.balances, sender), EInsufficientFunds);
        let bal = table::borrow_mut(&mut bank.balances, sender);
        assert!(*bal >= amount, EInsufficientFunds);
        *bal = *bal - amount;
        let coin = coin::from_balance(balance::split(&mut bank.pool, amount), ctx);
        transfer::public_transfer(coin, sender);
    }
}
