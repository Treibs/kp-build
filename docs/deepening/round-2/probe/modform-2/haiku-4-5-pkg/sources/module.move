module name_registry::registry {
    use std::string::String;
    use sui::table::Table;

    public struct Registry has key {
        id: UID,
        names: Table<String, address>,
    }

    public fun create(ctx: &mut TxContext) {
        let registry = Registry {
            id: object::new(ctx),
            names: sui::table::new(ctx),
        };
        transfer::share_object(registry);
    }

    public fun register(registry: &mut Registry, name: String, ctx: &TxContext) {
        assert!(!registry.names.contains(&name), 0);
        registry.names.add(name, ctx.sender());
    }

    public fun release(registry: &mut Registry, name: String, ctx: &TxContext) {
        assert!(registry.names.contains(&name), 1);
        let owner = *registry.names.borrow(&name);
        assert!(owner == ctx.sender(), 2);
        registry.names.remove(name);
    }
}
