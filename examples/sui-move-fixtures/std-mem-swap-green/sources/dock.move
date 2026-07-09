module std_mem_swap_green::dock {
    // In-place replacement of a non-copy struct field: hold the field as
    // an `Option` slot and use `std::option::swap(t: &mut Option<Element>,
    // e: Element): Element`, which installs the new value and returns the
    // old one.
    public struct Battery has store {
        charge: u64,
    }

    public struct Dock has store {
        slot: Option<Battery>,
    }

    public fun swap_in(d: &mut Dock, fresh: Battery): Battery {
        option::swap(&mut d.slot, fresh)
    }

    public fun charge(b: &Battery): u64 {
        b.charge
    }
}
