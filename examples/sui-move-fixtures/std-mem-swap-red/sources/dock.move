module std_mem_swap_red::dock {
    // There is no `std::mem` module in Move. Rust's
    // `std::mem::swap`/`replace` idiom for taking a non-copy value out of
    // a borrowed struct does not exist; Move's idiom is an `Option` slot
    // with `std::option::swap` (see the green fixture).
    public struct Battery has store {
        charge: u64,
    }

    public struct Dock has store {
        slot: Battery,
    }

    public fun swap_in(d: &mut Dock, fresh: Battery): Battery {
        let mut old = fresh;
        std::mem::swap(&mut d.slot, &mut old);
        old
    }
}
