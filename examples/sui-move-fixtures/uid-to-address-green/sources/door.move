module uid_to_address_green::door {
    // UID -> address is uid_to_address; whole-object -> address is
    // id_address; id_to_address takes the copyable ID, not a UID.
    public struct Invitation has key {
        id: UID,
    }

    public fun check_in(inv: &Invitation): (address, address) {
        (object::uid_to_address(&inv.id), object::id_address(inv))
    }
}
