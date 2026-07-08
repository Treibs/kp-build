module name_registry::registry {
    use std::string::{Self, String};
    use sui::table::{Self, Table};

    public struct Registry has key, store {
        id: UID,
        names: Table<String, address>,
    }

    fun init(ctx: &mut TxContext) {
        let registry = Registry {
            id: object::new(ctx),
            names: table::new(ctx),
        };
        transfer::share_object(registry);
    }

    public fun register(registry: &mut Registry, name: String, ctx: &TxContext) {
        assert!(!table::contains(&registry.names, name), 1);
        table::add(&mut registry.names, name, ctx.sender());
    }

    public fun release(registry: &mut Registry, name: String, ctx: &TxContext) {
        assert!(table::contains(&registry.names, name), 2);
        let owner = table::remove(&mut registry.names, name);
        assert!(owner == ctx.sender(), 3);
    }
}
