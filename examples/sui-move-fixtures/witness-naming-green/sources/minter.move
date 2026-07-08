module witness_naming_green::minter {
    // A plain (reusable) witness must NOT be named the upper-case module
    // name — that naming pattern is reserved for one-time witnesses.
    public struct MinterWitness has drop {}

    public fun witness(): MinterWitness {
        MinterWitness {}
    }

    public fun prove(_w: MinterWitness): bool {
        true
    }
}
