module beacon::status {
    use std::string::String;
    use sui::event;
    use sui::object::ID;

    public struct Beacon has key, store {
        id: UID,
        status: u8,
        note: String,
    }

    public struct BeaconCreated has copy, drop {
        beacon_id: ID,
        owner: address,
    }

    public struct StatusChanged has copy, drop {
        beacon_id: ID,
        new_status: u8,
        epoch: u64,
    }

    public fun create(note: String, ctx: &mut TxContext) -> Beacon {
        let beacon = Beacon {
            id: object::new(ctx),
            status: 0,
            note,
        };
        let beacon_id = object::id(&beacon);
        let owner = ctx.sender();
        
        event::emit(BeaconCreated {
            beacon_id,
            owner,
        });
        
        beacon
    }

    public fun set_status(beacon: &mut Beacon, new_status: u8, ctx: &mut TxContext) {
        beacon.status = new_status;
        
        event::emit(StatusChanged {
            beacon_id: object::id(beacon),
            new_status,
            epoch: ctx.epoch(),
        });
    }

    public fun set_note(beacon: &mut Beacon, note: String) {
        beacon.note = note;
    }
}
