module tuple_bleed_red::waitlist {
    public struct Board has key {
        id: UID,
        entries: vector<u64>,
    }

    // a tuple pushed into a type argument — tuples are expression/return
    // conveniences, not runtime values (see green: a named struct)
    public fun next_entry(board: &Board): Option<(u64, address)> {
        if (board.entries.is_empty()) option::none()
        else option::some((0, @0x0))
    }
}
