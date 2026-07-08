module transfer_composability_green::mint {
    public struct Badge has key, store { id: UID }

    // Returning the object (instead of transferring it to the sender)
    // lets a PTB caller pass it to any subsequent command.
    public fun new(ctx: &mut TxContext): Badge {
        Badge { id: object::new(ctx) }
    }
}
