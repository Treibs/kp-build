module ild::desk {
    use sui::table::{Self, Table};
    use sui::event;

    public struct Desk has key {
        id: UID,
        outstanding: Table<address, u64>,
        total_recalled: u64,
    }

    public struct AdminCap has key, store {
        id: UID,
    }

    public struct Volume has key, store {
        id: UID,
        home_library: address,
    }

    public struct LibraryCap has key, store {
        id: UID,
        library: address,
    }

    public struct VolumeRecalled has copy, drop {
        home_library: address,
        volume_id: ID,
    }

    public struct RecallAcknowledged has copy, drop {
        library: address,
        outstanding: u64,
    }

    fun init(ctx: &mut TxContext) {
        transfer::share_object(Desk {
            id: object::new(ctx),
            outstanding: table::new(ctx),
            total_recalled: 0,
        });
        transfer::transfer(AdminCap { id: object::new(ctx) }, ctx.sender());
    }

    public fun register_library(
        _cap: &AdminCap,
        library: address,
        desk: &mut Desk,
        ctx: &mut TxContext,
    ) {
        if (!table::contains(&desk.outstanding, library)) {
            table::add(&mut desk.outstanding, library, 0u64);
        };
        transfer::transfer(LibraryCap { id: object::new(ctx), library }, library);
    }

    public fun issue_volume(
        _cap: &AdminCap,
        home_library: address,
        ctx: &mut TxContext,
    ): Volume {
        Volume { id: object::new(ctx), home_library }
    }

    public fun recall(desk: &mut Desk, volume: Volume) {
        let home = volume.home_library;
        let vol_id = object::id(&volume);

        if (!table::contains(&desk.outstanding, home)) {
            table::add(&mut desk.outstanding, home, 0u64);
        };

        {
            let n = table::borrow_mut(&mut desk.outstanding, home);
            *n = *n + 1;
        };

        desk.total_recalled = desk.total_recalled + 1;

        event::emit(VolumeRecalled { home_library: home, volume_id: vol_id });

        transfer::public_transfer(volume, home);
    }

    public fun acknowledge(desk: &mut Desk, cap: &LibraryCap) {
        let lib = cap.library;
        assert!(table::contains(&desk.outstanding, lib), 0);
        let n = table::borrow_mut(&mut desk.outstanding, lib);
        assert!(*n > 0, 1);
        *n = *n - 1;
        let remaining = *n;
        event::emit(RecallAcknowledged { library: lib, outstanding: remaining });
    }

    public fun outstanding_recalls(desk: &Desk, library: address): u64 {
        if (table::contains(&desk.outstanding, library)) {
            *table::borrow(&desk.outstanding, library)
        } else {
            0
        }
    }

    public fun total_recalled(desk: &Desk): u64 {
        desk.total_recalled
    }
}
