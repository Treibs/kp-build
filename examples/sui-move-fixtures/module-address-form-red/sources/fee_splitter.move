// Bare `module name {` (no address qualifier) is the pre-2024 form and
// does not compile: Move 2024 requires `module <address>::<name>`.
module fee_splitter {
    public fun share(amount: u64, parts: u64): u64 {
        amount / parts
    }
}
