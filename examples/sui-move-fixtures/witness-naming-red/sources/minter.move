module witness_naming_red::minter {
    // Upper-case of the module name + no fields + only `drop` makes this a
    // one-time witness — which cannot be constructed manually.
    public struct MINTER has drop {}

    public fun witness(): MINTER {
        MINTER {}
    }
}
