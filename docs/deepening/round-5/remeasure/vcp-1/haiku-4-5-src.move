module food_truck::loyalty {
    use sui::balance::{Balance, self};
    use sui::coin::{Coin, self};
    use sui::sui::SUI;
    use sui::table::{Table, self};
    use sui::tx_context::{TxContext, sender};
    use sui::transfer;
    use sui::object::{UID, self};
    use std::option::{self, Option};

    public struct Truck has key, store {
        id: UID,
        meal_price: u64,
        pool: Balance<SUI>,
        punches: Table<address, u64>,
    }

    public struct AdminCap has key, store {
        id: UID,
    }

    public struct LOYALTY has drop {}

    fun init(_: LOYALTY, ctx: &mut TxContext) {
        let admin_cap = AdminCap {
            id: object::new(ctx),
        };
        transfer::transfer(admin_cap, sender(ctx));
    }

    public fun create_truck(meal_price: u64, ctx: &mut TxContext) {
        let truck = Truck {
            id: object::new(ctx),
            meal_price,
            pool: balance::zero(),
            punches: table::new(ctx),
        };
        transfer::share_object(truck);
    }

    public fun buy_meal(truck: &mut Truck, payment: Coin<SUI>, ctx: &mut TxContext): Option<Coin<SUI>> {
        let buyer = sender(ctx);
        let paid_amount = coin::value(&payment);
        
        let current_punches = if (table::contains(&truck.punches, buyer)) {
            *table::borrow(&truck.punches, buyer)
        } else {
            0
        };
        
        let new_punches = current_punches + 1;
        
        if (table::contains(&truck.punches, buyer)) {
            *table::borrow_mut(&mut truck.punches, buyer) = new_punches;
        } else {
            table::add(&mut truck.punches, buyer, new_punches);
        };
        
        if (new_punches % 5 == 0) {
            option::some(payment)
        } else {
            assert!(paid_amount == truck.meal_price, 1);
            let balance = coin::into_balance(payment);
            balance::join(&mut truck.pool, balance);
            option::none()
        }
    }

    public fun get_punches(truck: &Truck, buyer: address): u64 {
        if (table::contains(&truck.punches, buyer)) {
            *table::borrow(&truck.punches, buyer)
        } else {
            0
        }
    }

    public fun get_pool_total(truck: &Truck): u64 {
        balance::value(&truck.pool)
    }

    public fun sweep_pool(_cap: &AdminCap, truck: &mut Truck, ctx: &mut TxContext): Coin<SUI> {
        let amount = balance::value(&truck.pool);
        let balance = balance::split(&mut truck.pool, amount);
        coin::from_balance(balance, ctx)
    }
}
