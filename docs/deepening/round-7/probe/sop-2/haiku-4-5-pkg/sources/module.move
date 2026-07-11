module aquarium::tank_hall {
    use sui::object::{Self, UID, ID};
    use sui::tx_context::TxContext;
    use sui::transfer;
    use sui::clock::Clock;
    use sui::event;
    use std::option::{Self, Option};
    use std::vector;

    public struct AdminCap has key, store {
        id: UID,
    }

    public struct ExhibitInfo has store, drop {
        id: ID,
        label: vector<u8>,
    }

    public struct Tank has store {
        exhibit: Option<ExhibitInfo>,
    }

    public struct TankHall has key {
        id: UID,
        tanks: vector<Tank>,
    }

    public struct Stocked has copy, drop {
        tank_index: u64,
        exhibit_id: ID,
        timestamp_ms: u64,
    }

    fun init(ctx: &mut TxContext) {
        let cap = AdminCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, ctx.sender());

        let hall = TankHall {
            id: object::new(ctx),
            tanks: vector[],
        };
        transfer::share_object(hall);
    }

    public fun init_tanks(
        _cap: &AdminCap,
        hall: &mut TankHall,
        num_tanks: u64,
    ) {
        let mut i = 0;
        while (i < num_tanks) {
            vector::push_back(&mut hall.tanks, Tank {
                exhibit: option::none(),
            });
            i = i + 1;
        };
    }

    public fun stock_exhibit(
        _cap: &AdminCap,
        hall: &mut TankHall,
        tank_index: u64,
        exhibit_id: ID,
        label: vector<u8>,
        clock: &Clock,
    ) {
        let tank = vector::borrow_mut(&mut hall.tanks, tank_index);
        assert!(option::is_none(&tank.exhibit), 1);
        
        option::fill(&mut tank.exhibit, ExhibitInfo { id: exhibit_id, label });
        
        event::emit(Stocked {
            tank_index,
            exhibit_id,
            timestamp_ms: clock.timestamp_ms(),
        });
    }

    public fun retire_exhibit(
        _cap: &AdminCap,
        hall: &mut TankHall,
        tank_index: u64,
        clock: &Clock,
    ): ExhibitInfo {
        let tank = vector::borrow_mut(&mut hall.tanks, tank_index);
        let exhibit = option::extract(&mut tank.exhibit);
        
        event::emit(Stocked {
            tank_index,
            exhibit_id: exhibit.id,
            timestamp_ms: clock.timestamp_ms(),
        });
        
        exhibit
    }

    public fun move_exhibit(
        _cap: &AdminCap,
        hall: &mut TankHall,
        from_index: u64,
        to_index: u64,
        clock: &Clock,
    ) {
        let from_tank = vector::borrow_mut(&mut hall.tanks, from_index);
        let exhibit = option::extract(&mut from_tank.exhibit);
        
        let to_tank = vector::borrow_mut(&mut hall.tanks, to_index);
        assert!(option::is_none(&to_tank.exhibit), 2);
        
        option::fill(&mut to_tank.exhibit, exhibit);
        
        event::emit(Stocked {
            tank_index: to_index,
            exhibit_id: exhibit.id,
            timestamp_ms: clock.timestamp_ms(),
        });
    }

    public fun has_exhibit(hall: &TankHall, tank_index: u64): bool {
        let tank = vector::borrow(&hall.tanks, tank_index);
        option::is_some(&tank.exhibit)
    }

    public fun get_exhibit_id(hall: &TankHall, tank_index: u64): Option<ID> {
        let tank = vector::borrow(&hall.tanks, tank_index);
        if (option::is_some(&tank.exhibit)) {
            let exhibit = option::borrow(&tank.exhibit);
            option::some(exhibit.id)
        } else {
            option::none()
        }
    }

    public fun count_stocked(hall: &TankHall): u64 {
        let mut count = 0;
        let mut i = 0;
        while (i < vector::length(&hall.tanks)) {
            let tank = vector::borrow(&hall.tanks, i);
            if (option::is_some(&tank.exhibit)) {
                count = count + 1;
            };
            i = i + 1;
        };
        count
    }
}
