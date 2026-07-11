module aquarium::tank_hall {
    use sui::event;
    use sui::clock::Clock;
    use sui::table::{Self, Table};
    use std::string::{Self, String};
    use std::option::{Self, Option};

    public struct WardenCap has key, store {
        id: UID,
    }

    public struct Exhibit has store {
        exhibit_id: u64,
        label: String,
        stocked_at_ms: u64,
    }

    public struct TankHall has key {
        id: UID,
        num_tanks: u64,
        exhibits: Table<u64, Exhibit>,
    }

    public struct Stocked has copy, drop {
        tank_number: u64,
        exhibit_id: u64,
        label: String,
        timestamp_ms: u64,
    }

    public fun create(num_tanks: u64, ctx: &mut TxContext): WardenCap {
        transfer::share_object(TankHall {
            id: object::new(ctx),
            num_tanks,
            exhibits: table::new(ctx),
        });
        WardenCap { id: object::new(ctx) }
    }

    public fun stock(
        _cap: &WardenCap,
        hall: &mut TankHall,
        tank_number: u64,
        exhibit_id: u64,
        label: vector<u8>,
        clock: &Clock,
    ) {
        assert!(tank_number < hall.num_tanks);
        assert!(!table::contains(&hall.exhibits, tank_number));
        let timestamp_ms = clock.timestamp_ms();
        let label_str = string::utf8(label);
        table::add(&mut hall.exhibits, tank_number, Exhibit {
            exhibit_id,
            label: label_str,
            stocked_at_ms: timestamp_ms,
        });
        event::emit(Stocked { tank_number, exhibit_id, label: label_str, timestamp_ms });
    }

    public fun retire(
        _cap: &WardenCap,
        hall: &mut TankHall,
        tank_number: u64,
    ) {
        assert!(table::contains(&hall.exhibits, tank_number));
        let Exhibit { exhibit_id: _, label: _, stocked_at_ms: _ } =
            table::remove(&mut hall.exhibits, tank_number);
    }

    public fun move_exhibit(
        _cap: &WardenCap,
        hall: &mut TankHall,
        from_tank: u64,
        to_tank: u64,
        clock: &Clock,
    ) {
        assert!(table::contains(&hall.exhibits, from_tank));
        assert!(!table::contains(&hall.exhibits, to_tank));
        let mut exhibit = table::remove(&mut hall.exhibits, from_tank);
        let timestamp_ms = clock.timestamp_ms();
        exhibit.stocked_at_ms = timestamp_ms;
        let exhibit_id = exhibit.exhibit_id;
        let label = exhibit.label;
        table::add(&mut hall.exhibits, to_tank, exhibit);
        event::emit(Stocked { tank_number: to_tank, exhibit_id, label, timestamp_ms });
    }

    public fun exhibit_label(hall: &TankHall, tank_number: u64): Option<String> {
        if (table::contains(&hall.exhibits, tank_number)) {
            option::some(table::borrow(&hall.exhibits, tank_number).label)
        } else {
            option::none()
        }
    }

    public fun stocked_count(hall: &TankHall): u64 {
        table::length(&hall.exhibits)
    }
}
