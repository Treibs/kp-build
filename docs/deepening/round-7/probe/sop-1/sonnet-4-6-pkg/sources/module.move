module lighthouse::station {
    use sui::clock::Clock;
    use sui::event;
    use std::option::{Self, Option};

    public struct LighthouseStation has key {
        id: UID,
        keeper: Option<address>,
        handover_count: u64,
    }

    public struct HarborAuthorityCap has key, store {
        id: UID,
    }

    public struct Handover has copy, drop {
        timestamp_ms: u64,
        new_keeper: address,
    }

    fun init(ctx: &mut TxContext) {
        transfer::transfer(HarborAuthorityCap { id: object::new(ctx) }, ctx.sender());
        transfer::share_object(LighthouseStation {
            id: object::new(ctx),
            keeper: option::none(),
            handover_count: 0,
        });
    }

    /// Outgoing keeper installs the incoming keeper directly.
    public fun keeper_handover(
        station: &mut LighthouseStation,
        new_keeper: address,
        clock: &Clock,
        ctx: &TxContext,
    ) {
        assert!(option::is_some(&station.keeper));
        assert!(*option::borrow(&station.keeper) == ctx.sender());
        let _ = option::swap(&mut station.keeper, new_keeper);
        station.handover_count = station.handover_count + 1;
        event::emit(Handover { timestamp_ms: clock.timestamp_ms(), new_keeper });
    }

    /// Harbor authority installs a keeper when the station is vacant.
    public fun authority_handover(
        station: &mut LighthouseStation,
        _cap: &HarborAuthorityCap,
        new_keeper: address,
        clock: &Clock,
    ) {
        assert!(option::is_none(&station.keeper));
        option::fill(&mut station.keeper, new_keeper);
        station.handover_count = station.handover_count + 1;
        event::emit(Handover { timestamp_ms: clock.timestamp_ms(), new_keeper });
    }

    /// Current keeper vacates the station, leaving it unmanned between rotations.
    public fun vacate(station: &mut LighthouseStation, ctx: &TxContext) {
        assert!(option::is_some(&station.keeper));
        assert!(*option::borrow(&station.keeper) == ctx.sender());
        let _ = option::extract(&mut station.keeper);
    }

    /// Returns the current keeper's address if the station is manned.
    public fun current_keeper(station: &LighthouseStation): Option<address> {
        station.keeper
    }

    /// Returns the total number of handovers logged.
    public fun handover_count(station: &LighthouseStation): u64 {
        station.handover_count
    }
}
