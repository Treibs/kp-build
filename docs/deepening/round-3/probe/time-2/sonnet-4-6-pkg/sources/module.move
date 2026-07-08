module timelock::strongbox {
    use sui::coin::Coin;
    use sui::sui::SUI;
    use sui::clock::Clock;

    public struct Strongbox has key {
        id: UID,
        coin: Coin<SUI>,
        unlock_at_ms: u64,
    }

    public fun lock(
        deposit: Coin<SUI>,
        unlock_at_ms: u64,
        heir: address,
        ctx: &mut TxContext,
    ) {
        let box = Strongbox {
            id: object::new(ctx),
            coin: deposit,
            unlock_at_ms,
        };
        transfer::transfer(box, heir);
    }

    public fun open(
        strongbox: Strongbox,
        clock: &Clock,
        ctx: &mut TxContext,
    ) {
        let Strongbox { id, coin, unlock_at_ms } = strongbox;
        assert!(clock.timestamp_ms() >= unlock_at_ms);
        object::delete(id);
        transfer::public_transfer(coin, ctx.sender());
    }
}
