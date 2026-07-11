module lighthouse::log {
    use sui::clock::Clock;
    use sui::event;
    use std::option::{Self, Option};

    public struct AdminCap has key, store {
        id: UID,
    }

    public struct Station has key {
        id: UID,
        current_keeper: Option<address>,
        handover_count: u64,
    }

    public struct Handover has copy, drop {
        new_keeper: address,
        timestamp_ms: u64,
    }

    fun init(ctx: &mut TxContext) {
        let station = Station {
            id: object::new(ctx),
            current_keeper: option::none(),
            handover_count: 0,
        };
        transfer::share_object(station);

        let admin_cap = AdminCap {
            id: object::new(ctx),
        };
        transfer::transfer(admin_cap, tx_context::sender(ctx));
    }

    public fun handover_by_keeper(
        station: &mut Station,
        new_keeper: address,
        clock: &Clock,
        ctx: &mut TxContext,
    ) {
        let sender = tx_context::sender(ctx);
        
        assert!(option::is_some(&station.current_keeper), 1);
        assert!(option::borrow(&station.current_keeper) == &sender, 2);
        
        let timestamp_ms = clock.timestamp_ms();
        station.current_keeper = option::some(new_keeper);
        station.handover_count = station.handover_count + 1;
        
        event::emit(Handover {
            new_keeper,
            timestamp_ms,
        });
    }

    public fun handover_by_authority(
        station: &mut Station,
        new_keeper: address,
        clock: &Clock,
        _cap: &AdminCap,
    ) {
        assert!(option::is_none(&station.current_keeper), 3);
        
        let timestamp_ms = clock.timestamp_ms();
        station.current_keeper = option::some(new_keeper);
        station.handover_count = station.handover_count + 1;
        
        event::emit(Handover {
            new_keeper,
            timestamp_ms,
        });
    }

    public fun current_keeper(station: &Station): Option<address> {
        station.current_keeper
    }

    public fun handover_count(station: &Station): u64 {
        station.handover_count
    }
}
