module mentorship::registry {
    use std::option::{Self, Option};
    use sui::table::{Self, Table};

    public struct LeadCap has key, store {
        id: UID,
    }

    public struct Registry has key {
        id: UID,
        mentees: Table<address, Option<address>>,
        matched_count: u64,
    }

    fun init(ctx: &mut TxContext) {
        transfer::transfer(LeadCap { id: object::new(ctx) }, ctx.sender());
        transfer::share_object(Registry {
            id: object::new(ctx),
            mentees: table::new(ctx),
            matched_count: 0,
        });
    }

    public fun enroll(registry: &mut Registry, ctx: &mut TxContext) {
        let mentee = ctx.sender();
        assert!(!table::contains(&registry.mentees, mentee));
        table::add(&mut registry.mentees, mentee, option::none());
    }

    public fun match_mentee(
        registry: &mut Registry,
        _cap: &LeadCap,
        mentee: address,
        mentor: address,
    ) {
        let is_new = option::is_none(table::borrow(&registry.mentees, mentee));
        if (is_new) {
            option::fill(table::borrow_mut(&mut registry.mentees, mentee), mentor);
            registry.matched_count = registry.matched_count + 1;
        } else {
            let _ = option::swap(table::borrow_mut(&mut registry.mentees, mentee), mentor);
        };
    }

    public fun unmatch(
        registry: &mut Registry,
        _cap: &LeadCap,
        mentee: address,
    ) {
        let was_matched = option::is_some(table::borrow(&registry.mentees, mentee));
        if (was_matched) {
            let _ = option::extract(table::borrow_mut(&mut registry.mentees, mentee));
            registry.matched_count = registry.matched_count - 1;
        };
    }

    public fun get_mentor(registry: &Registry, mentee: address): Option<address> {
        if (table::contains(&registry.mentees, mentee)) {
            *table::borrow(&registry.mentees, mentee)
        } else {
            option::none()
        }
    }

    public fun matched_count(registry: &Registry): u64 {
        registry.matched_count
    }
}
