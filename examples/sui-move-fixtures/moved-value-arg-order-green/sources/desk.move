module moved_value_arg_order_green::desk {
    public struct Parcel has key {
        id: UID,
        addressee: address,
    }

    // arguments evaluate left to right and the move happens first:
    // read every field you need into locals BEFORE the value moves
    public fun dispatch(parcel: Parcel) {
        let destination = parcel.addressee;
        transfer::transfer(parcel, destination)
    }
}
