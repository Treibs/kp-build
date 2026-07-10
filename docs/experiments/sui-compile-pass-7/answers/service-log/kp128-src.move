module appliance_repair::shop {
    use sui::object::{Self, ID, UID};
    use sui::tx_context::TxContext;
    use sui::transfer;
    use sui::table::{Self, Table};
    use sui::event;
    use std::vector;
    
    public struct SHOP has drop {}
    
    public struct Appliance has key {
        id: UID,
        owner: address,
    }
    
    public struct ShopState has key {
        id: UID,
        histories: Table<ID, vector<Service>>,
        total_visits: u64,
    }
    
    public struct MechanicCap has key, store {
        id: UID,
    }
    
    public struct Service has store, copy, drop {
        epoch: u64,
        note: vector<u8>,
    }
    
    public struct ServiceLogged has copy, drop {
        appliance_id: address,
        visit_count: u64,
    }
    
    public struct Scrapped has copy, drop {
        appliance_id: address,
        final_visit_count: u64,
    }
    
    fun init(_witness: SHOP, ctx: &mut TxContext) {
        let shop = ShopState {
            id: object::new(ctx),
            histories: table::new(ctx),
            total_visits: 0,
        };
        transfer::share_object(shop);
        
        let cap = MechanicCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, ctx.sender());
    }
    
    public fun create_appliance(ctx: &mut TxContext): Appliance {
        Appliance {
            id: object::new(ctx),
            owner: ctx.sender(),
        }
    }
    
    public fun log_service(
        appliance: &Appliance,
        shop: &mut ShopState,
        _cap: &MechanicCap,
        epoch: u64,
        note: vector<u8>,
    ) {
        let appliance_id = object::uid_to_inner(&appliance.id);
        
        if (!table::contains(&shop.histories, appliance_id)) {
            table::add(&mut shop.histories, appliance_id, vector[]);
        };
        
        let history = table::borrow_mut(&mut shop.histories, appliance_id);
        vector::push_back(history, Service { epoch, note });
        
        shop.total_visits = shop.total_visits + 1;
        
        event::emit(ServiceLogged {
            appliance_id: object::id_to_address(&appliance_id),
            visit_count: vector::length(history),
        });
    }
    
    public fun get_visit_count(appliance: &Appliance, shop: &ShopState): u64 {
        let appliance_id = object::uid_to_inner(&appliance.id);
        if (table::contains(&shop.histories, appliance_id)) {
            vector::length(table::borrow(&shop.histories, appliance_id))
        } else {
            0
        }
    }
    
    public fun get_total_visits(shop: &ShopState): u64 {
        shop.total_visits
    }
    
    public fun scrap_appliance(
        appliance: Appliance,
        shop: &mut ShopState,
    ) {
        let Appliance { id, owner: _ } = appliance;
        let appliance_id = object::uid_to_inner(&id);
        
        let final_visit_count = if (table::contains(&shop.histories, appliance_id)) {
            let history = table::remove(&mut shop.histories, appliance_id);
            vector::length(&history)
        } else {
            0
        };
        
        object::delete(id);
        
        event::emit(Scrapped {
            appliance_id: object::id_to_address(&appliance_id),
            final_visit_count,
        });
    }
}
