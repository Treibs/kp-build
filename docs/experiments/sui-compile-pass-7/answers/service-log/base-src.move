module appliance_shop::service {
    use sui::object::{Self, UID, ID};
    use sui::tx_context::TxContext;
    use sui::table::{Self, Table};
    use sui::event;
    use sui::vector;

    struct ServiceHistory has key {
        id: UID,
        visits: Table<ID, vector<ServiceVisit>>,
        total_visits: u64,
    }

    struct ServiceVisit has store, copy, drop {
        epoch: u64,
        note: vector<u8>,
    }

    struct MechanicCap has key {
        id: UID,
    }

    struct ScrapEvent has copy, drop {
        appliance_id: ID,
        final_visit_count: u64,
    }

    fun init(ctx: &mut TxContext) {
        let service_history = ServiceHistory {
            id: object::new(ctx),
            visits: table::new(ctx),
            total_visits: 0,
        };
        sui::transfer::share_object(service_history);
    }

    public fun log_visit(
        history: &mut ServiceHistory,
        _cap: &MechanicCap,
        appliance_id: ID,
        epoch: u64,
        note: vector<u8>,
    ) {
        let visit = ServiceVisit { epoch, note };
        
        if (!table::contains(&history.visits, appliance_id)) {
            table::add(&mut history.visits, appliance_id, vector::empty());
        }
        
        let visits = table::borrow_mut(&mut history.visits, appliance_id);
        vector::push_back(visits, visit);
        history.total_visits = history.total_visits + 1;
    }

    public fun get_visit_count(history: &ServiceHistory, appliance_id: ID): u64 {
        if (table::contains(&history.visits, appliance_id)) {
            vector::length(table::borrow(&history.visits, appliance_id))
        } else {
            0
        }
    }

    public fun get_total_visits(history: &ServiceHistory): u64 {
        history.total_visits
    }

    public fun scrap_appliance(
        history: &mut ServiceHistory,
        appliance_id: ID,
    ) {
        let final_count = get_visit_count(history, appliance_id);
        
        if (table::contains(&history.visits, appliance_id)) {
            let _visits = table::remove(&mut history.visits, appliance_id);
            history.total_visits = history.total_visits - final_count;
        }
        
        event::emit(ScrapEvent {
            appliance_id,
            final_visit_count: final_count,
        });
    }
}
