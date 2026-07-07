module receiving_red::mailbox {
    use receiving_red::parcel::Parcel;

    public struct Mailbox has key {
        id: UID,
    }

    public fun redeem(mailbox: &mut Mailbox, ticket: transfer::Receiving<Parcel>): Parcel {
        // internal `receive` outside Parcel's defining module
        transfer::receive(&mut mailbox.id, ticket)
    }
}
