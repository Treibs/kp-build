module capsule::capsule {
    use std::string::String;
    use std::option;

    public struct Gift has key, store {
        id: UID,
        message: String,
    }

    public struct TimeCapsule has key {
        id: UID,
        gift: option::Option<Gift>,
        unlock_epoch: u64,
    }

    public fun create(unlock_epoch: u64, ctx: &mut TxContext): TimeCapsule {
        TimeCapsule {
            id: object::new(ctx),
            gift: option::none(),
            unlock_epoch,
        }
    }

    public fun bury(capsule: &mut TimeCapsule, gift: Gift) {
        assert!(!option::is_some(&capsule.gift), 1);
        capsule.gift = option::some(gift);
    }

    public fun unearth(capsule: &mut TimeCapsule, ctx: &mut TxContext) {
        let current_epoch = ctx.epoch();
        assert!(current_epoch >= capsule.unlock_epoch, 2);
        assert!(option::is_some(&capsule.gift), 3);
        let gift = option::extract(&mut capsule.gift);
        transfer::public_transfer(gift, ctx.sender());
    }

    public fun discard_empty(capsule: TimeCapsule) {
        let TimeCapsule { id, gift, unlock_epoch: _ } = capsule;
        assert!(!option::is_some(&gift), 4);
        option::destroy_none(gift);
        object::delete(id);
    }
}
