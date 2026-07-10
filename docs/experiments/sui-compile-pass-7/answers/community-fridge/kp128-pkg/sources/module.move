module fridge::community {
    use std::string::String;
    use sui::event;
    use sui::table::{Self, Table};
    use std::vector;
    use std::option::{Self, Option};
    use sui::tx_context;

    public struct Meal has key, store {
        id: UID,
        label: String,
        epoch_stocked: u64,
    }

    public struct Fridge has key {
        id: UID,
        meals: vector<Meal>,
        current_epoch: u64,
        taken_this_epoch: Table<address, u64>,
    }

    public struct CoordinatorCap has key, store {
        id: UID,
    }

    public struct MealDiscarded has copy, drop {
        meal_id: ID,
        label: String,
    }

    fun init(ctx: &mut TxContext) {
        let fridge = Fridge {
            id: object::new(ctx),
            meals: vector[],
            current_epoch: 0,
            taken_this_epoch: table::new(ctx),
        };
        transfer::share_object(fridge);

        let cap = CoordinatorCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, tx_context::sender(ctx));
    }

    public fun stock_meal(
        fridge: &mut Fridge,
        label: String,
        ctx: &mut TxContext,
    ) {
        let meal = Meal {
            id: object::new(ctx),
            label,
            epoch_stocked: fridge.current_epoch,
        };
        vector::push_back(&mut fridge.meals, meal);
    }

    public fun take_meal(
        fridge: &mut Fridge,
        ctx: &mut TxContext,
    ): Option<Meal> {
        let sender = tx_context::sender(ctx);
        
        if (table::contains(&fridge.taken_this_epoch, sender)) {
            let last_took_epoch = table::borrow(&fridge.taken_this_epoch, sender);
            if (*last_took_epoch >= fridge.current_epoch) {
                return option::none()
            };
        };

        if (vector::is_empty(&fridge.meals)) {
            return option::none()
        };

        let meal = vector::pop_back(&mut fridge.meals);
        
        if (table::contains(&fridge.taken_this_epoch, sender)) {
            *table::borrow_mut(&mut fridge.taken_this_epoch, sender) = fridge.current_epoch;
        } else {
            table::add(&mut fridge.taken_this_epoch, sender, fridge.current_epoch);
        };
        
        option::some(meal)
    }

    public fun advance_epoch(
        fridge: &mut Fridge,
        _cap: &CoordinatorCap,
    ) {
        fridge.current_epoch = fridge.current_epoch + 1;
    }

    public fun sweep_spoilage(
        fridge: &mut Fridge,
        _cap: &CoordinatorCap,
    ) {
        let mut i = 0;
        while (i < vector::length(&fridge.meals)) {
            let meal = vector::borrow(&fridge.meals, i);
            if (meal.epoch_stocked < fridge.current_epoch) {
                let discarded = vector::remove(&mut fridge.meals, i);
                let Meal { id, label, epoch_stocked: _ } = discarded;
                event::emit(MealDiscarded {
                    meal_id: object::uid_to_inner(&id),
                    label,
                });
                object::delete(id);
            } else {
                i = i + 1;
            };
        };
    }
}
