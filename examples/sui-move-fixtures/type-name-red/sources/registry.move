module type_name_red::registry {
    use std::string::String;
    use std::type_name;

    public struct Registry has key {
        id: UID,
        // Wrong: type reflection does not return std::string::String.
        recorded: vector<String>,
    }

    public fun record<T>(reg: &mut Registry) {
        reg.recorded.push_back(type_name::with_defining_ids<T>());
    }
}
