module interlibrary_loan::desk {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::TxContext;
    use sui::table::{Self, Table};

    public struct Volume has key, store {
        id: UID,
        home_library: address,
    }

    public struct LibraryCap has key, store {
        id: UID,
        library: address,
    }

    public struct RecallDesk has key {
        id: UID,
        outstanding_recalls: Table<address, u64>,
        total_recalled: Table<address, u64>,
    }

    fun init(ctx: &mut TxContext) {
        let desk = RecallDesk {
            id: object::new(ctx),
            outstanding_recalls: table::new(ctx),
            total_recalled: table::new(ctx),
        };
        transfer::share_object(desk);
    }

    public fun create_library_cap(library: address, ctx: &mut TxContext): LibraryCap {
        LibraryCap {
            id: object::new(ctx),
            library,
        }
    }

    public fun lend_volume(home_library: address, ctx: &mut TxContext): Volume {
        Volume {
            id: object::new(ctx),
            home_library,
        }
    }

    public fun recall(
        desk: &mut RecallDesk,
        volume: Volume,
    ) {
        let home_library = volume.home_library;
        
        let outstanding = get_outstanding_recalls(desk, home_library);
        update_outstanding_recalls(&mut desk.outstanding_recalls, home_library, outstanding + 1);

        let total = get_total_recalled(desk, home_library);
        update_total_recalled(&mut desk.total_recalled, home_library, total + 1);

        transfer::transfer(volume, home_library);
    }

    public fun acknowledge_recall(
        desk: &mut RecallDesk,
        cap: &LibraryCap,
    ) {
        let outstanding = get_outstanding_recalls(desk, cap.library);
        if (outstanding > 0) {
            update_outstanding_recalls(&mut desk.outstanding_recalls, cap.library, outstanding - 1);
        }
    }

    public fun get_outstanding_recalls(desk: &RecallDesk, library: address): u64 {
        if (table::contains(&desk.outstanding_recalls, library)) {
            *table::borrow(&desk.outstanding_recalls, library)
        } else {
            0
        }
    }

    public fun get_total_recalled(desk: &RecallDesk, library: address): u64 {
        if (table::contains(&desk.total_recalled, library)) {
            *table::borrow(&desk.total_recalled, library)
        } else {
            0
        }
    }

    fun update_outstanding_recalls(table: &mut Table<address, u64>, library: address, count: u64) {
        if (table::contains(table, library)) {
            table::remove(table, library);
        };
        table::add(table, library, count);
    }

    fun update_total_recalled(table: &mut Table<address, u64>, library: address, count: u64) {
        if (table::contains(table, library)) {
            table::remove(table, library);
        };
        table::add(table, library, count);
    }
}
