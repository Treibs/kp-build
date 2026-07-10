module reference_type_argument_green::door {
    // store the copyable identity, not a reference; borrow at use
    public struct Stamp has key {
        id: UID,
    }

    public struct Gate has key {
        id: UID,
        last_stamp: Option<ID>,
    }

    public fun record(gate: &mut Gate, stamp: &Stamp) {
        option::swap_or_fill(&mut gate.last_stamp, object::id(stamp));
    }
}
