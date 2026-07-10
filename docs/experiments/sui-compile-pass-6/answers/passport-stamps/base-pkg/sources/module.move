module event_passport::passport {
    use sui::object::{Self, UID, ID};
    use sui::tx_context::{Self, TxContext};
    use sui::transfer;
    use sui::vec_set::{Self, VecSet};

    public struct Passport has key, store {
        id: UID,
        stamps: VecSet<ID>,
    }

    public struct VenueCap has key {
        id: UID,
    }

    public struct Badge has key {
        id: UID,
        passport_id: ID,
    }

    public fun mint_passport(ctx: &mut TxContext) {
        transfer::transfer(
            Passport {
                id: object::new(ctx),
                stamps: vec_set::empty(),
            },
            tx_context::sender(ctx),
        )
    }

    public fun create_venue_cap(ctx: &mut TxContext) {
        transfer::transfer(
            VenueCap {
                id: object::new(ctx),
            },
            tx_context::sender(ctx),
        )
    }

    public fun stamp_passport(
        passport: &mut Passport,
        venue_cap: &VenueCap,
    ) {
        let venue_id = object::id(venue_cap);
        assert!(!vec_set::contains(&passport.stamps, &venue_id), 1);
        vec_set::insert(&mut passport.stamps, venue_id);
    }

    public fun redeem_badge(passport: Passport, ctx: &mut TxContext): Badge {
        assert!(vec_set::size(&passport.stamps) == 5, 2);
        let passport_id = object::id(&passport);
        let Passport { id, stamps: _ } = passport;
        object::delete(id);
        Badge {
            id: object::new(ctx),
            passport_id,
        }
    }
}
