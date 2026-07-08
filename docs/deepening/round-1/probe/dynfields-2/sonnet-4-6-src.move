module ledger::ledger {
    use sui::table::{Self, Table};

    const EInsufficientBalance: u64 = 0;

    public struct Ledger has key {
        id: UID,
        balances: Table<address, u64>,
    }

    fun init(ctx: &mut TxContext) {
        transfer::share_object(Ledger {
            id: object::new(ctx),
            balances: table::new(ctx),
        });
    }

    public fun credit(ledger: &mut Ledger, who: address, amount: u64) {
        if (table::contains(&ledger.balances, who)) {
            let balance = table::borrow_mut(&mut ledger.balances, who);
            *balance = *balance + amount;
        } else {
            table::add(&mut ledger.balances, who, amount);
        }
    }

    public fun debit(ledger: &mut Ledger, who: address, amount: u64) {
        assert!(table::contains(&ledger.balances, who), EInsufficientBalance);
        let balance = table::borrow_mut(&mut ledger.balances, who);
        assert!(*balance >= amount, EInsufficientBalance);
        *balance = *balance - amount;
        if (*balance == 0) {
            table::remove(&mut ledger.balances, who);
        }
    }
}
