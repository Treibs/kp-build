module std_table_path_green::registry {
    use sui::table::{Self, Table};

    public struct Registry has key {
        id: UID,
        entries: Table<address, u64>,
    }

    public fun new_registry(ctx: &mut TxContext): Registry {
        Registry { id: object::new(ctx), entries: table::new(ctx) }
    }

    public fun count(registry: &Registry): u64 {
        table::length(&registry.entries)
    }
}
