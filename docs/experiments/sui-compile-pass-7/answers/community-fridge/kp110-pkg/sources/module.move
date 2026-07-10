module 0x0::fridge {
    use sui::event;
    use sui::clock::Clock;
    use std::string::String;

    public struct Meal has key, store {
        id: UID,
        label: String,
        epoch_stocked: u64,
    }

    public struct Fridge has key {
        id: UID,
        meals: vector<Meal>,
        current_epoch: u64,
    }

    public struct AdminCap has key, store {
        id: UID,
    }

    public struct MealDiscarded has copy, drop {
        meal_id: ID,
        label: String,
        epoch_stocked: u64,
    }

    fun init(ctx: &mut TxContext) {
        let admin_cap = AdminCap {
            id: object::new(ctx),
        };
        transfer::transfer(admin_cap, ctx.sender());

        let fridge = Fridge {
            id: object::new(ctx),
            meals: vector[],
            current_epoch: 0,
        };
        transfer::share_object(fridge);
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
        fridge.meals.push_back(meal);
    }

    public fun take_meal(
        fridge: &mut Fridge,
        index: u64,
    ): Meal {
        fridge.meals.remove(index)
    }

    public fun spoilage_sweep(
        fridge: &mut Fridge,
        _cap: &AdminCap,
        clock: &Clock,
    ) {
        let current_time = clock.timestamp_ms();
        let epoch_duration = 86400000;
        let new_epoch = current_time / epoch_duration;

        let mut i = 0;
        while (i < fridge.meals.length()) {
            if (fridge.meals[i].epoch_stocked < new_epoch) {
                let removed = fridge.meals.remove(i);
                let meal_id = object::id(&removed);
                let Meal { id, label, epoch_stocked } = removed;
                event::emit(MealDiscarded {
                    meal_id,
                    label,
                    epoch_stocked,
                });
                object::delete(id);
            } else {
                i = i + 1;
            }
        }

        fridge.current_epoch = new_epoch;
    }
}
