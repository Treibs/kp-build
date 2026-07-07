module receiving_green::mailbox {
    public struct Mailbox has key {
        id: UID,
    }

    public struct Parcel has key, store {
        id: UID,
    }

    /// Redeem a parcel that was sent to the mailbox object's address.
    public fun redeem(mailbox: &mut Mailbox, ticket: transfer::Receiving<Parcel>): Parcel {
        transfer::public_receive(&mut mailbox.id, ticket)
    }
}
