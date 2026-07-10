module apple_press::press {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::table::{Self, Table};
    use std::vector;

    public struct Press has key {
        id: UID,
        yield_rate: u64,
        total_weight: u64,
        pressed: bool,
        household_weights: Table<address, u64>,
    }

    public struct CiderJug has key, store {
        id: UID,
        amount: u64,
    }

    public struct KeeperCap has key, store {
        id: UID,
    }

    public fun create_press(yield_rate: u64, ctx: &mut TxContext): (Press, KeeperCap) {
        let press = Press {
            id: object::new(ctx),
            yield_rate,
            total_weight: 0,
            pressed: false,
            household_weights: table::new(ctx),
        };

        let cap = KeeperCap {
            id: object::new(ctx),
        };

        (press, cap)
    }

    public fun deposit(
        press: &mut Press,
        weight: u64,
        ctx: &mut TxContext,
    ) {
        assert!(!press.pressed, 0);

        let sender = tx_context::sender(ctx);
        press.total_weight = press.total_weight + weight;

        if (table::contains(&press.household_weights, sender)) {
            let w = table::borrow_mut(&mut press.household_weights, sender);
            *w = *w + weight;
        } else {
            table::add(&mut press.household_weights, sender, weight);
        };
    }

    public fun execute_press(
        _cap: &KeeperCap,
        press: &mut Press,
        households: vector<address>,
        ctx: &mut TxContext,
    ) {
        assert!(!press.pressed, 1);
        press.pressed = true;

        let total_cider = ((press.total_weight as u128) * (press.yield_rate as u128) / 1000) as u64;
        let mut distributed = 0u64;

        let mut i = 0;
        while (i < vector::length(&households)) {
            let household = *vector::borrow(&households, i);

            let weight = if (table::contains(&press.household_weights, household)) {
                *table::borrow(&press.household_weights, household)
            } else {
                0
            };

            let share = if (press.total_weight > 0) {
                ((weight as u128) * (total_cider as u128) / (press.total_weight as u128)) as u64
            } else {
                0
            };

            distributed = distributed + share;

            let jug = CiderJug {
                id: object::new(ctx),
                amount: share,
            };
            transfer::public_transfer(jug, household);

            i = i + 1;
        };

        let keeper_address = tx_context::sender(ctx);
        let keeper_share = total_cider - distributed;
        let keeper_jug = CiderJug {
            id: object::new(ctx),
            amount: keeper_share,
        };
        transfer::public_transfer(keeper_jug, keeper_address);
    }

    public fun weight_waiting(press: &Press): u64 {
        press.total_weight
    }

    public fun is_pressed(press: &Press): bool {
        press.pressed
    }

    public fun jug_amount(jug: &CiderJug): u64 {
        jug.amount
    }
}
