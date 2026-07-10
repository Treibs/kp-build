module uid_to_address_red::door {
    // id_to_address takes an &ID; feeding it the object's &UID is the
    // shape the probe wrote (see uid-to-address-green for the fix).
    public struct Invitation has key {
        id: UID,
    }

    public fun check_in(inv: &Invitation): address {
        object::id_to_address(&inv.id)
    }
}
