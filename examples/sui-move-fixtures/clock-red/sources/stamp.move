module clock_red::stamp {
    public struct Stamp has key {
        id: UID,
        created_ms: u64,
    }

    public fun create(ctx: &mut TxContext) {
        // Fabricated API: TxContext has no clock; time comes from `sui::clock::Clock`.
        transfer::transfer(
            Stamp { id: object::new(ctx), created_ms: tx_context::now_ms(ctx) },
            ctx.sender(),
        )
    }
}
