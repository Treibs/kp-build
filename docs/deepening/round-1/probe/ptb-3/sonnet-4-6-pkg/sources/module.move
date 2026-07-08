module airdrop::airdrop {
    public struct Badge has key, store {
        id: UID,
        serial: u64,
    }

    public entry fun claim(serial: u64, recipient: Option<address>, ctx: &mut TxContext) {
        let badge = Badge {
            id: object::new(ctx),
            serial,
        };
        let to = if (recipient.is_some()) {
            recipient.destroy_some()
        } else {
            ctx.sender()
        };
        transfer::public_transfer(badge, to);
    }
}
