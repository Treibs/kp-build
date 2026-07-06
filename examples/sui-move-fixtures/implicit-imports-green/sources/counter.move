module implicit_imports_green::counter {
    // No `use sui::object::...`, `use sui::transfer`, or `use sui::tx_context::...`:
    // UID, object, transfer, TxContext are implicit in edition 2024.
    public struct Counter has key {
        id: UID,
        value: u64,
    }

    public fun create(ctx: &mut TxContext) {
        transfer::share_object(Counter { id: object::new(ctx), value: 0 })
    }
}
