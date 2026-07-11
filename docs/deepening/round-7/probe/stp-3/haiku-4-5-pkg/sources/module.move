module apiary::hive {
    use sui::object::{Self, UID};
    use sui::table::{Self, Table};
    use sui::transfer;
    use sui::tx_context::TxContext;

    public struct AdminCap has key, store {
        id: UID,
    }

    public struct HiveStand has store {
        stand_number: u64,
        keeper: address,
        queen_line: u64,
        total_weight: u64,
    }

    public struct Apiary has key {
        id: UID,
        stands: Table<u64, HiveStand>,
        keeper_stands_count: Table<address, u64>,
        next_stand_number: u64,
    }

    public struct StandView has drop, copy {
        keeper: address,
        queen_line: u64,
        total_weight: u64,
    }

    fun init(ctx: &mut TxContext) {
        let apiary = Apiary {
            id: object::new(ctx),
            stands: table::new(ctx),
            keeper_stands_count: table::new(ctx),
            next_stand_number: 1,
        };
        transfer::share_object(apiary);

        let admin_cap = AdminCap {
            id: object::new(ctx),
        };
        transfer::transfer(admin_cap, ctx.sender());
    }

    public fun assign_stand(
        apiary: &mut Apiary,
        _admin_cap: &AdminCap,
        keeper: address,
        queen_line: u64,
    ) {
        let stand = HiveStand {
            stand_number: apiary.next_stand_number,
            keeper,
            queen_line,
            total_weight: 0,
        };

        table::add(&mut apiary.stands, apiary.next_stand_number, stand);

        if (table::contains(&apiary.keeper_stands_count, keeper)) {
            let count = table::borrow(&apiary.keeper_stands_count, keeper);
            let new_count = *count + 1;
            *table::borrow_mut(&mut apiary.keeper_stands_count, keeper) = new_count;
        } else {
            table::add(&mut apiary.keeper_stands_count, keeper, 1);
        };

        apiary.next_stand_number = apiary.next_stand_number + 1;
    }

    public fun log_honey(
        apiary: &mut Apiary,
        stand_number: u64,
        weight: u64,
        ctx: &TxContext,
    ) {
        let stand = table::borrow_mut(&mut apiary.stands, stand_number);
        assert!(stand.keeper == ctx.sender(), 1);
        stand.total_weight = stand.total_weight + weight;
    }

    public fun vacate_and_reassign(
        apiary: &mut Apiary,
        _admin_cap: &AdminCap,
        stand_number: u64,
        new_keeper: address,
        new_queen_line: u64,
    ) {
        let stand = table::borrow_mut(&mut apiary.stands, stand_number);
        let old_keeper = stand.keeper;

        stand.keeper = new_keeper;
        stand.queen_line = new_queen_line;
        stand.total_weight = 0;

        let old_count = *table::borrow(&apiary.keeper_stands_count, old_keeper) - 1;
        *table::borrow_mut(&mut apiary.keeper_stands_count, old_keeper) = old_count;

        if (table::contains(&apiary.keeper_stands_count, new_keeper)) {
            let count = table::borrow(&apiary.keeper_stands_count, new_keeper);
            let new_count = *count + 1;
            *table::borrow_mut(&mut apiary.keeper_stands_count, new_keeper) = new_count;
        } else {
            table::add(&mut apiary.keeper_stands_count, new_keeper, 1);
        };
    }

    public fun stand_view(apiary: &Apiary, stand_number: u64): StandView {
        let stand = table::borrow(&apiary.stands, stand_number);
        StandView {
            keeper: stand.keeper,
            queen_line: stand.queen_line,
            total_weight: stand.total_weight,
        }
    }

    public fun keeper_stands_count(apiary: &Apiary, keeper: address): u64 {
        if (table::contains(&apiary.keeper_stands_count, keeper)) {
            *table::borrow(&apiary.keeper_stands_count, keeper)
        } else {
            0
        }
    }
}
