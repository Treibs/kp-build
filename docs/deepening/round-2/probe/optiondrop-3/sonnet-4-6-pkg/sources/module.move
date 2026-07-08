module capsule::capsule {
    use std::string::String;

    public struct Gift has key, store {
        id: UID,
        message: String,
    }

    public struct TimeCapsule has key {
        id: UID,
        gift: Option<Gift>,
        unlock_epoch: u64,
    }

    public fun create(unlock_epoch: u64, ctx: &mut TxContext): TimeCapsule {
        TimeCapsule {
            id: object::new(ctx),
            gift: option::none(),
            unlock_epoch,
        }
    }

    public fun new_gift(message: String, ctx: &mut TxContext): Gift {
        Gift {
            id: object::new(ctx),
            message,
        }
    }

    public fun bury(capsule: &mut TimeCapsule, gift: Gift) {
        assert!(capsule.gift.is_none());
        capsule.gift.fill(gift);
    }

    public fun unearth(capsule: &mut TimeCapsule, ctx: &mut TxContext) {
        assert!(ctx.epoch() >= capsule.unlock_epoch);
        let gift = capsule.gift.extract();
        transfer::transfer(gift, ctx.sender());
    }

    public fun discard_empty(capsule: TimeCapsule) {
        let TimeCapsule { id, gift, unlock_epoch: _ } = capsule;
        assert!(gift.is_none());
        gift.destroy_none();
        id.delete();
    }
}
