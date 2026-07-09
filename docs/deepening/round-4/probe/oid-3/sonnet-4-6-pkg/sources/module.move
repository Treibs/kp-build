module wreck::permit {
    use std::string::String;
    use sui::event;
    use sui::object::ID;

    public struct Building has key {
        id: UID,
        street: String,
        floors: u64,
    }

    public struct CityCap has key {
        id: UID,
    }

    public struct SalvageReceipt has key {
        id: UID,
        building_id: ID,
        floors_salvaged: u64,
    }

    public struct Demolished has copy, drop {
        building_id: ID,
        street: String,
    }

    fun init(ctx: &mut TxContext) {
        transfer::transfer(CityCap { id: object::new(ctx) }, ctx.sender());
    }

    public fun construct(street: String, floors: u64, ctx: &mut TxContext): Building {
        Building {
            id: object::new(ctx),
            street,
            floors,
        }
    }

    public fun demolish(_cap: &CityCap, building: Building, ctx: &mut TxContext): SalvageReceipt {
        let Building { id, street, floors } = building;
        let building_id = object::uid_to_inner(&id);
        event::emit(Demolished { building_id, street });
        object::delete(id);
        SalvageReceipt {
            id: object::new(ctx),
            building_id,
            floors_salvaged: floors,
        }
    }
}
