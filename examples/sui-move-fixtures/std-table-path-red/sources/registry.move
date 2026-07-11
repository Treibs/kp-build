module std_table_path_red::registry {
    // Table is a Sui framework container — there is no std::table
    use std::table::{Self, Table};

    public struct Registry has key {
        id: UID,
        entries: Table<address, u64>,
    }

    public fun count(registry: &Registry): u64 {
        table::length(&registry.entries)
    }
}
