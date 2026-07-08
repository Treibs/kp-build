module type_name_green::registry {
    use std::type_name::{Self, TypeName};

    public struct Registry has key {
        id: UID,
        // Type reflection yields TypeName values, not strings.
        recorded: vector<TypeName>,
    }

    public fun record<T>(reg: &mut Registry) {
        // On sui 1.74.1 `type_name::get` is deprecated (renamed);
        // `with_defining_ids` is the current form and returns TypeName.
        reg.recorded.push_back(type_name::with_defining_ids<T>());
    }

    public fun label<T>(): std::ascii::String {
        // Converting a TypeName to a string yields std::ascii::String.
        type_name::with_defining_ids<T>().into_string()
    }
}
