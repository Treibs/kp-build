module interlibrary_loan_desk::system {
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;
    use sui::table::{Self, Table};
    use sui::event;
    use sui::transfer;

    public struct Desk has key {
        id: UID,
        outstanding_recalls: Table<address, u64>,
        total_recalled: Table<address, u64>,
    }

    public struct Volume has key, store {
        id: UID,
        home_library: address,
    }

    public struct LibraryCap has key {
        id: UID,
        library: address,
    }

    public struct RecalledEvent has copy, drop {
        volume_id: address,
        library: address,
    }

    public struct AcknowledgedEvent has copy, drop {
        library: address,
    }

    fun init(ctx: &mut TxContext) {
        let desk = Desk {
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

    public fun issue_volume(home_library: address, ctx: &mut TxContext): Volume {
        Volume {
            id: object::new(ctx),
            home_library,
        }
    }

    public fun recall_volume(desk: &mut Desk, volume: &Volume) {
        let library = volume.home_library;
        
        if (!table::contains(&desk.outstanding_recalls, library)) {
            table::add(&mut desk.outstanding_recalls, library, 0);
        };
        
        {
            let count = table::borrow_mut(&mut desk.outstanding_recalls, library);
            *count = *count + 1;
        };

        if (!table::contains(&desk.total_recalled, library)) {
            table::add(&mut desk.total_recalled, library, 0);
        };
        
        {
            let total = table::borrow_mut(&mut desk.total_recalled, library);
            *total = *total + 1;
        };

        event::emit(RecalledEvent {
            volume_id: object::uid_to_inner(&volume.id),
            library,
        });
    }

    public fun acknowledge_recall(desk: &mut Desk, _cap: &LibraryCap) {
        let library = _cap.library;
        
        if (table::contains(&desk.outstanding_recalls, library)) {
            let count = table::borrow_mut(&mut desk.outstanding_recalls, library);
            if (*count > 0) {
                *count = *count - 1;
            };
        };

        event::emit(AcknowledgedEvent { library });
    }

    public fun get_outstanding_recalls(desk: &Desk, library: address): u64 {
        if (table::contains(&desk.outstanding_recalls, library)) {
            *table::borrow(&desk.outstanding_recalls, library)
        } else {
            0
        }
    }

    public fun get_total_recalled(desk: &Desk, library: address): u64 {
        if (table::contains(&desk.total_recalled, library)) {
            *table::borrow(&desk.total_recalled, library)
        } else {
            0
        }
    }
}
