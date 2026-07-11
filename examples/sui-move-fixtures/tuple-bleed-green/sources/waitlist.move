module tuple_bleed_green::waitlist {
    // paired data that must live in a container gets a named struct —
    // tuples cannot be type arguments or stored values
    public struct Entry has copy, drop, store {
        pos: u64,
        who: address,
    }

    public struct Board has key {
        id: UID,
        entries: vector<Entry>,
    }

    public fun next_entry(board: &Board): Option<Entry> {
        if (board.entries.is_empty()) option::none()
        else option::some(board.entries[0])
    }

    public fun entry_fields(entry: &Entry): (u64, address) {
        // a bare tuple RETURN is fine — tuples fail only as type
        // arguments or stored values
        (entry.pos, entry.who)
    }
}
