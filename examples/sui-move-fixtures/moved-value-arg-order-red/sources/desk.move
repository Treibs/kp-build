module moved_value_arg_order_red::desk {
    public struct Parcel has key {
        id: UID,
        addressee: address,
    }

    // the parcel moves as the first argument, then the second argument
    // reads a field from the moved value (see green: hoist the read)
    public fun dispatch(parcel: Parcel) {
        transfer::transfer(parcel, parcel.addressee)
    }
}
