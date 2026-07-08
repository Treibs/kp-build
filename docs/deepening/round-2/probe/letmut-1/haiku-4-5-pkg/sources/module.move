module mint::batch {
    public struct Ticket has key, store {
        id: UID,
        serial: u64,
    }

    public fun mint_batch(count: u64, recipient: address, ctx: &mut TxContext) {
        let mut i = 0;
        while (i < count) {
            let ticket = Ticket {
                id: object::new(ctx),
                serial: i,
            };
            transfer::public_transfer(ticket, recipient);
            i = i + 1;
        }
    }
}
