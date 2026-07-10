module repair_shop::service {
    use std::vector;
    use sui::table::{Self, Table};
    use sui::event;
    use sui::transfer;
    use sui::tx_context::TxContext;

    public struct Visit has store, copy, drop {
        epoch: u64,
        note: vector<u8>,
    }

    public struct ServiceHistory has key {
        id: UID,
        visits: Table<address, vector<Visit>>,
        total_visits: u64,
    }

    public struct MechanicCap has key, store {
        id: UID,
    }

    public struct Scrapped has copy, drop {
        appliance_id: address,
        final_visit_count: u64,
    }

    fun init(ctx: &mut TxContext) {
        let history = ServiceHistory {
            id: object::new(ctx),
            visits: table::new(ctx),
            total_visits: 0,
        };
        transfer::share_object(history);

        let cap = MechanicCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, ctx.sender());
    }

    public fun record_visit(
        history: &mut ServiceHistory,
        _cap: &MechanicCap,
        appliance_id: address,
        epoch: u64,
        note: vector<u8>,
    ) {
        let visit = Visit { epoch, note };

        if (!table::contains(&history.visits, appliance_id)) {
            table::add(&mut history.visits, appliance_id, vector[visit]);
        } else {
            let visits = table::borrow_mut(&mut history.visits, appliance_id);
            vector::push_back(visits, visit);
        };

        history.total_visits = history.total_visits + 1;
    }

    public fun get_visit_count(
        history: &ServiceHistory,
        appliance_id: address,
    ): u64 {
        if (table::contains(&history.visits, appliance_id)) {
            vector::length(table::borrow(&history.visits, appliance_id))
        } else {
            0
        }
    }

    public fun total_visits(
        history: &ServiceHistory,
    ): u64 {
        history.total_visits
    }

    public fun scrap_appliance(
        history: &mut ServiceHistory,
        appliance_id: address,
    ) {
        let count = get_visit_count(history, appliance_id);

        if (table::contains(&history.visits, appliance_id)) {
            let _ = table::remove(&mut history.visits, appliance_id);
        };

        event::emit(Scrapped {
            appliance_id,
            final_visit_count: count,
        });
    }
}
