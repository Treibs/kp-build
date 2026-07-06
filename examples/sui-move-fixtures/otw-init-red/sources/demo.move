module otw_init_red::demo {
    public struct Registry has key {
        id: UID,
    }

    // Wrong init signature: first parameter is not a one-time witness.
    fun init(value: u64, ctx: &mut TxContext) {
        let _ = value;
        transfer::share_object(Registry { id: object::new(ctx) })
    }
}
