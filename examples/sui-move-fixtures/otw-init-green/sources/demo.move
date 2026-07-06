module otw_init_green::demo {
    /// One-time witness: same name as the module, uppercased, `drop` only.
    public struct DEMO has drop {}

    public struct Registry has key {
        id: UID,
    }

    fun init(_witness: DEMO, ctx: &mut TxContext) {
        transfer::share_object(Registry { id: object::new(ctx) })
    }
}
