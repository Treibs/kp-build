module clock_green::stamp {
    use sui::clock::Clock;

    public struct Stamp has key {
        id: UID,
        created_ms: u64,
    }

    public fun create(clock: &Clock, ctx: &mut TxContext) {
        transfer::transfer(
            Stamp { id: object::new(ctx), created_ms: clock.timestamp_ms() },
            ctx.sender(),
        )
    }
}
