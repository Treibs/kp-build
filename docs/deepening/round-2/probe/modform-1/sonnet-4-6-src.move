module rate_limiter::limiter {
    use sui::table::{Self, Table};

    public struct Limiter has key {
        id: UID,
        last_ping: Table<address, u64>,
    }

    public fun create(ctx: &mut TxContext) {
        transfer::share_object(Limiter {
            id: object::new(ctx),
            last_ping: table::new(ctx),
        });
    }

    entry fun ping(limiter: &mut Limiter, ctx: &mut TxContext) {
        let sender = ctx.sender();
        let epoch = ctx.epoch();
        if (table::contains(&limiter.last_ping, sender)) {
            let last = table::borrow_mut(&mut limiter.last_ping, sender);
            assert!(*last != epoch);
            *last = epoch;
        } else {
            table::add(&mut limiter.last_ping, sender, epoch);
        }
    }
}
