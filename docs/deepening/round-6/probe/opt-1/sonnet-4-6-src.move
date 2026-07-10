module clinic::scheduler {
    use sui::table::{Self, Table};

    public struct AdminCap has key, store {
        id: UID,
    }

    public struct Calendar has key {
        id: UID,
        slots: vector<Option<address>>,
        patient_epoch: Table<address, u64>,
        epoch: u64,
    }

    fun init(ctx: &mut TxContext) {
        transfer::transfer(AdminCap { id: object::new(ctx) }, ctx.sender());
    }

    public fun create(_cap: &AdminCap, slot_count: u64, ctx: &mut TxContext) {
        let mut slots = vector<Option<address>>[];
        let mut i = 0;
        while (i < slot_count) {
            vector::push_back(&mut slots, option::none());
            i = i + 1;
        };
        transfer::share_object(Calendar {
            id: object::new(ctx),
            slots,
            patient_epoch: table::new(ctx),
            epoch: 0,
        });
    }

    public fun book(calendar: &mut Calendar, slot: u64, ctx: &mut TxContext) {
        let patient = ctx.sender();
        let current_epoch = calendar.epoch;
        if (table::contains(&calendar.patient_epoch, patient)) {
            assert!(*table::borrow(&calendar.patient_epoch, patient) != current_epoch);
        };
        assert!(slot < vector::length(&calendar.slots));
        assert!(option::is_none(vector::borrow(&calendar.slots, slot)));
        *vector::borrow_mut(&mut calendar.slots, slot) = option::some(patient);
        if (table::contains(&calendar.patient_epoch, patient)) {
            *table::borrow_mut(&mut calendar.patient_epoch, patient) = current_epoch;
        } else {
            table::add(&mut calendar.patient_epoch, patient, current_epoch);
        }
    }

    public fun cancel(_cap: &AdminCap, calendar: &mut Calendar, slot: u64) {
        assert!(slot < vector::length(&calendar.slots));
        assert!(option::is_some(vector::borrow(&calendar.slots, slot)));
        *vector::borrow_mut(&mut calendar.slots, slot) = option::none();
    }

    public fun advance_epoch(_cap: &AdminCap, calendar: &mut Calendar) {
        calendar.epoch = calendar.epoch + 1;
        let n = vector::length(&calendar.slots);
        let mut i = 0;
        while (i < n) {
            *vector::borrow_mut(&mut calendar.slots, i) = option::none();
            i = i + 1;
        }
    }

    public fun slot_holder(calendar: &Calendar, slot: u64): Option<address> {
        assert!(slot < vector::length(&calendar.slots));
        *vector::borrow(&calendar.slots, slot)
    }

    public fun next_free_slot(calendar: &Calendar): Option<u64> {
        let n = vector::length(&calendar.slots);
        let mut i = 0;
        while (i < n) {
            if (option::is_none(vector::borrow(&calendar.slots, i))) {
                return option::some(i)
            };
            i = i + 1;
        };
        option::none()
    }
}
