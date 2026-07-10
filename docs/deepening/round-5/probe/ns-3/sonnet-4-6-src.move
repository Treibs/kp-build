module medication_tracker::cabinet {
    use sui::clock::Clock;

    const MIN_INTERVAL_MS: u64 = 14_400_000; // 4 hours
    const E_TOO_SOON: u64 = 0;

    public struct Cabinet has key {
        id: UID,
        last_dose_ms: u64,
        total_doses: u64,
    }

    public fun create(ctx: &mut TxContext): Cabinet {
        Cabinet {
            id: object::new(ctx),
            last_dose_ms: 0,
            total_doses: 0,
        }
    }

    public fun log_dose(cabinet: &mut Cabinet, clock: &Clock) {
        let now = clock.timestamp_ms();
        if (cabinet.last_dose_ms != 0) {
            assert!(now - cabinet.last_dose_ms >= MIN_INTERVAL_MS, E_TOO_SOON);
        };
        cabinet.last_dose_ms = now;
        cabinet.total_doses = cabinet.total_doses + 1;
    }

    public fun last_dose_ms(cabinet: &Cabinet): u64 {
        cabinet.last_dose_ms
    }

    public fun total_doses(cabinet: &Cabinet): u64 {
        cabinet.total_doses
    }
}
