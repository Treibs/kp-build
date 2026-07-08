module rate_limiter::limiter {
    use sui::dynamic_field;

    public struct Limiter has key {
        id: UID,
    }

    public fun create_and_share(ctx: &mut TxContext) {
        let limiter = Limiter {
            id: object::new(ctx),
        };
        transfer::share_object(limiter);
    }

    public fun ping(limiter: &mut Limiter, ctx: &mut TxContext) {
        let sender = tx_context::sender(ctx);
        let current_epoch = tx_context::epoch(ctx);
        
        if (dynamic_field::exists<address>(&limiter.id, sender)) {
            let last_epoch = dynamic_field::remove<address, u64>(&mut limiter.id, sender);
            assert!(last_epoch < current_epoch, 0);
        };
        
        dynamic_field::add(&mut limiter.id, sender, current_epoch);
    }
}
