module wine_cellar::cellar {
    use sui::object::{Self, UID};
    use sui::tx_context::{Self, TxContext};
    use sui::transfer;
    use std::vector;
    use std::string::String;

    public struct Bottle has key, store {
        id: UID,
        vintage_year: u16,
        label: String,
        owner: address,
    }

    public struct WineCellar has key {
        id: UID,
        bottles: vector<Bottle>,
    }

    public struct SommelierCapability has key {
        id: UID,
        reserve_list: vector<u16>,
    }

    public fun create_cellar(ctx: &mut TxContext) {
        let cellar = WineCellar {
            id: object::new(ctx),
            bottles: vector::empty(),
        };
        transfer::share_object(cellar);
    }

    public fun create_sommelier_capability(sommelier: address, ctx: &mut TxContext) {
        let capability = SommelierCapability {
            id: object::new(ctx),
            reserve_list: vector::empty(),
        };
        transfer::transfer(capability, sommelier);
    }

    public fun rack_bottle(
        cellar: &mut WineCellar,
        vintage_year: u16,
        label: String,
        ctx: &mut TxContext,
    ) {
        let bottle = Bottle {
            id: object::new(ctx),
            vintage_year,
            label,
            owner: tx_context::sender(ctx),
        };
        vector::push_back(&mut cellar.bottles, bottle);
    }

    public fun unrack_bottle(
        cellar: &mut WineCellar,
        bottle_idx: u64,
        ctx: &mut TxContext,
    ) {
        let sender = tx_context::sender(ctx);
        let bottle = vector::remove(&mut cellar.bottles, bottle_idx);
        assert!(bottle.owner == sender, 0);
        transfer::transfer(bottle, sender);
    }

    public fun add_to_reserve(
        capability: &mut SommelierCapability,
        vintage: u16,
    ) {
        vector::push_back(&mut capability.reserve_list, vintage);
    }

    public fun is_on_reserve(capability: &SommelierCapability, vintage: u16): bool {
        vector::contains(&capability.reserve_list, &vintage)
    }

    public fun oldest_bottle(cellar: &WineCellar): (u16, String) {
        assert!(!vector::is_empty(&cellar.bottles), 0);
        
        let mut oldest_idx = 0;
        let mut oldest_year = vector::borrow(&cellar.bottles, 0).vintage_year;
        let len = vector::length(&cellar.bottles);
        
        let mut i = 1;
        while (i < len) {
            let bottle = vector::borrow(&cellar.bottles, i);
            if (bottle.vintage_year < oldest_year) {
                oldest_year = bottle.vintage_year;
                oldest_idx = i;
            };
            i = i + 1;
        };
        
        let bottle = vector::borrow(&cellar.bottles, oldest_idx);
        (bottle.vintage_year, bottle.label)
    }
}
