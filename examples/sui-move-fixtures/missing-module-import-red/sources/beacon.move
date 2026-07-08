module missing_module_import_red::beacon {
    // Rust resolves `mod::fn` paths without a per-module import; Move 2024
    // does not. `event::emit` with no `use sui::event` leaves the alias
    // `event` unbound.

    public struct Ping has copy, drop { value: u64 }

    public fun announce(value: u64) {
        event::emit(Ping { value });
    }
}
