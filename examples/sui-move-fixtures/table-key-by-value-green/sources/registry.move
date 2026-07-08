module table_key_by_value_green::registry {
    use std::string::String;
    use sui::table::Table;

    // `sui::table` takes keys BY VALUE (`K: copy + drop + store`), not by
    // reference: pass the `String` itself.
    public fun taken(names: &Table<String, address>, name: String): bool {
        names.contains(name)
    }
}
