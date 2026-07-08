module bank::bank {
    use sui::balance::{Balance, Self};
    use sui::coin::{Coin, Self};
    use sui::sui::SUI;
    use sui::table::{Table, Self};
    use sui::tx_context::{TxContext, sender};

    const INSUFFICIENT_BALANCE: u64 = 0;

    public struct Bank has key {
        id: UID,
        pool: Balance<SUI>,
        accounts: Table<address, u64>,
    }

    public fun new(ctx: &mut TxContext): Bank {
        Bank {
            id: object::new(ctx),
            pool: balance::zero(),
            accounts: table::new(ctx),
        }
    }

    public fun deposit(bank: &mut Bank, coin: Coin<SUI>, ctx: &TxContext) {
        let amount = coin::value(&coin);
        balance::join(&mut bank.pool, coin::into_balance(coin));
        
        let addr = sender(ctx);
        if (table::contains(&bank.accounts, addr)) {
            let current = table::borrow_mut(&mut bank.accounts, addr);
            *current = *current + amount;
        } else {
            table::add(&mut bank.accounts, addr, amount);
        };
    }

    public entry fun withdraw(bank: &mut Bank, amount: u64, ctx: &mut TxContext) {
        let addr = sender(ctx);
        
        assert!(table::contains(&bank.accounts, addr), INSUFFICIENT_BALANCE);
        
        let current = table::borrow_mut(&mut bank.accounts, addr);
        assert!(*current >= amount, INSUFFICIENT_BALANCE);
        *current = *current - amount;
        
        let coin = coin::from_balance(balance::split(&mut bank.pool, amount), ctx);
        transfer::public_transfer(coin, addr);
    }
}
