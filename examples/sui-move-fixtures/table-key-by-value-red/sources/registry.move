module table_key_by_value_red::registry {
    use std::string::String;
    use sui::table::Table;

    // Rust habit: passing the key by reference. `sui::table` key
    // parameters are by value, so `&name` is the wrong type.
    public fun taken(names: &Table<String, address>, name: String): bool {
        names.contains(&name)
    }
}
