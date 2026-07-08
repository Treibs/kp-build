module airdrop::airdrop {
    use std::option::{self, Option};

    public struct Badge has key, store {
        id: UID,
        serial: u64,
    }

    public fun claim(serial: u64, recipient: Option<address>, ctx: &mut TxContext) {
        let badge = Badge {
            id: object::new(ctx),
            serial,
        };

        let target = if (option::is_some(&recipient)) {
            option::destroy_some(recipient)
        } else {
            option::destroy_none(recipient);
            ctx.sender()
        };

        transfer::public_transfer(badge, target);
    }
}
