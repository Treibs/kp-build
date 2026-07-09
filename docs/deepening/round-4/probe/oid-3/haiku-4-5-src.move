module wreck::permit {
    use std::string::{Self, String};
    use sui::event;
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;

    public struct Building has key, store {
        id: UID,
        street: String,
        floors: u64,
    }

    public struct CityCap has key, store {
        id: UID,
    }

    public struct Demolished has copy, drop {
        street: vector<u8>,
        floors: u64,
    }

    public struct SalvageReceipt has key, store {
        id: UID,
        street: String,
        floors_salvaged: u64,
    }

    public fun construct(street: String, floors: u64, ctx: &mut TxContext): Building {
        Building {
            id: object::new(ctx),
            street,
            floors,
        }
    }

    public fun demolish(building: Building, _cap: &CityCap, ctx: &mut TxContext): SalvageReceipt {
        let Building { id, street, floors } = building;
        
        event::emit(Demolished {
            street: *string::bytes(&street),
            floors,
        });
        
        object::delete(id);
        
        SalvageReceipt {
            id: object::new(ctx),
            street,
            floors_salvaged: floors,
        }
    }
}
