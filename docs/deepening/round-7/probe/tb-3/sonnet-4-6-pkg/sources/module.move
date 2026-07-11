module tram_depot::tram {
    use sui::event;

    public struct DispatcherCap has key, store {
        id: UID,
    }

    public struct ShiftRecord has copy, drop, store {
        route: u64,
        driver: address,
    }

    public struct Tram has key {
        id: UID,
        shifts: vector<ShiftRecord>,
    }

    public struct DayClosed has copy, drop {
        tram_id: ID,
        route: u64,
        driver: address,
    }

    fun init(ctx: &mut TxContext) {
        transfer::transfer(DispatcherCap { id: object::new(ctx) }, ctx.sender());
    }

    public fun create_tram(ctx: &mut TxContext) {
        transfer::share_object(Tram {
            id: object::new(ctx),
            shifts: vector[],
        });
    }

    public fun log_shift(
        _cap: &DispatcherCap,
        tram: &mut Tram,
        route: u64,
        driver: address,
    ) {
        tram.shifts.push_back(ShiftRecord { route, driver });
    }

    public fun close_day(tram: &Tram) {
        let tram_id = object::uid_to_inner(&tram.id);
        let n = tram.shifts.length();
        if (n == 0) {
            event::emit(DayClosed { tram_id, route: 0, driver: @0x0 });
        } else {
            let last = *tram.shifts.borrow(n - 1);
            event::emit(DayClosed { tram_id, route: last.route, driver: last.driver });
        };
    }

    public fun total_shifts(tram: &Tram): u64 {
        tram.shifts.length()
    }
}
