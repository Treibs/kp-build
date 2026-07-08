module missing_module_import_green::beacon {
    // Calling a function through a module alias (`event::emit`) requires
    // the alias to be bound by a `use` declaration first.
    use sui::event;

    public struct Ping has copy, drop { value: u64 }

    public fun announce(value: u64) {
        event::emit(Ping { value });
    }
}
