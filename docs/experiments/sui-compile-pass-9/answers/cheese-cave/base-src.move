module cheese_cave::cave {
    use sui::object::{Self, UID};
    use sui::tx_context::{Self, TxContext};
    use sui::table::{Self, Table};
    use sui::event;
    use sui::transfer;
    use std::vector::{Self};

    public struct Ripened has copy, drop {
        maker: address,
        label: vector<u8>,
    }

    public struct Wheel has store {
        label: vector<u8>,
        ready_epoch: u64,
        maker: address,
    }

    public struct CheeseCave has key {
        id: UID,
        wheels: vector<Wheel>,
        resting_counts: Table<address, u64>,
    }

    public struct AffineurCapability has key {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        let cave = CheeseCave {
            id: object::new(ctx),
            wheels: vector::empty(),
            resting_counts: table::new(ctx),
        };
        
        let cap = AffineurCapability {
            id: object::new(ctx),
        };
        
        transfer::share_object(cave);
        transfer::transfer(cap, tx_context::sender(ctx));
    }

    public fun shelve(
        cave: &mut CheeseCave,
        label: vector<u8>,
        ready_epoch: u64,
        ctx: &mut TxContext,
    ) {
        let maker = tx_context::sender(ctx);
        
        let wheel = Wheel {
            label,
            ready_epoch,
            maker,
        };
        
        vector::push_back(&mut cave.wheels, wheel);
        
        let count = if (table::contains(&cave.resting_counts, maker)) {
            table::remove(&mut cave.resting_counts, maker) + 1
        } else {
            1
        };
        
        table::add(&mut cave.resting_counts, maker, count);
    }

    public fun ripen(
        cave: &mut CheeseCave,
        _cap: &AffineurCapability,
        wheel_index: u64,
        current_epoch: u64,
    ) {
        let wheel = vector::remove(&mut cave.wheels, wheel_index);
        
        assert!(current_epoch >= wheel.ready_epoch, 1);
        
        let Wheel { label, ready_epoch: _, maker } = wheel;
        
        let count = table::remove(&mut cave.resting_counts, maker);
        if (count > 1) {
            table::add(&mut cave.resting_counts, maker, count - 1);
        };
        
        event::emit(Ripened {
            maker,
            label,
        });
    }

    public fun resting_count(
        cave: &CheeseCave,
        maker: address,
    ): u64 {
        if (table::contains(&cave.resting_counts, maker)) {
            *table::borrow(&cave.resting_counts, maker)
        } else {
            0
        }
    }

    public fun oldest_wheel(
        cave: &CheeseCave,
    ): (vector<u8>, u64) {
        assert!(!vector::is_empty(&cave.wheels), 2);
        
        let mut oldest_idx = 0;
        let mut oldest_epoch = vector::borrow(&cave.wheels, 0).ready_epoch;
        let mut idx = 1;
        let len = vector::length(&cave.wheels);
        
        while (idx < len) {
            let current_epoch = vector::borrow(&cave.wheels, idx).ready_epoch;
            if (current_epoch < oldest_epoch) {
                oldest_idx = idx;
                oldest_epoch = current_epoch;
            };
            idx = idx + 1;
        };
        
        let oldest_wheel_ref = vector::borrow(&cave.wheels, oldest_idx);
        let mut label_copy = vector::empty();
        let label_len = vector::length(&oldest_wheel_ref.label);
        let mut i = 0;
        while (i < label_len) {
            vector::push_back(&mut label_copy, *vector::borrow(&oldest_wheel_ref.label, i));
            i = i + 1;
        };
        
        (label_copy, oldest_wheel_ref.ready_epoch)
    }
}
