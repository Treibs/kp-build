module beacon::status {
    use std::string::String;
    use sui::event;

    public struct Beacon has key {
        id: UID,
        status_code: u8,
        note: String,
    }

    public struct BeaconCreated has copy, drop {
        beacon_id: ID,
        owner: address,
    }

    public struct StatusChanged has copy, drop {
        beacon_id: ID,
        new_status_code: u8,
        epoch: u64,
    }

    public fun create(status_code: u8, note: String, ctx: &mut TxContext) {
        let beacon = Beacon {
            id: object::new(ctx),
            status_code,
            note,
        };
        let beacon_id = object::id(&beacon);
        event::emit(BeaconCreated {
            beacon_id,
            owner: ctx.sender(),
        });
        transfer::transfer(beacon, ctx.sender());
    }

    public fun set_status(beacon: &mut Beacon, new_status_code: u8, ctx: &mut TxContext) {
        beacon.status_code = new_status_code;
        event::emit(StatusChanged {
            beacon_id: object::id(beacon),
            new_status_code,
            epoch: ctx.epoch(),
        });
    }

    public fun set_note(beacon: &mut Beacon, new_note: String, ctx: &mut TxContext) {
        beacon.note = new_note;
        event::emit(StatusChanged {
            beacon_id: object::id(beacon),
            new_status_code: beacon.status_code,
            epoch: ctx.epoch(),
        });
    }
}
