// Move 2024: a module is declared with its package address (or named
// address) and its name: `module <address>::<name>`.
module module_address_form_green::fee_splitter {
    public fun share(amount: u64, parts: u64): u64 {
        amount / parts
    }
}
