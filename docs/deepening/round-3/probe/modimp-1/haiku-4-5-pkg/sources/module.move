module depot::inventory {
    use std::string::String;
    use sui::table::{Self, Table};

    public struct Depot has key {
        id: UID,
        goods: Table<String, u64>,
    }

    public struct OperatorCap has key, store {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        let depot = Depot {
            id: object::new(ctx),
            goods: table::new(ctx),
        };

        let cap = OperatorCap {
            id: object::new(ctx),
        };

        transfer::share_object(depot);
        transfer::transfer(cap, ctx.sender());
    }

    public fun restock(
        depot: &mut Depot,
        _cap: &OperatorCap,
        name: String,
        qty: u64,
    ) {
        if (table::contains(&depot.goods, name)) {
            let current = table::borrow_mut(&mut depot.goods, name);
            *current = *current + qty;
        } else {
            table::add(&mut depot.goods, name, qty);
        }
    }

    public fun consume(depot: &mut Depot, name: String) {
        assert!(table::contains(&depot.goods, name));
        let count = table::borrow_mut(&mut depot.goods, name);
        assert!(*count > 0);
        *count = *count - 1;
    }

    public fun stock(depot: &Depot, name: String): u64 {
        if (table::contains(&depot.goods, name)) {
            *table::borrow(&depot.goods, name)
        } else {
            0
        }
    }
}
