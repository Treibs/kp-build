module std_option_path_red::slot {
    // Option lives in the standard library — there is no sui::option
    use sui::option::{Self, Option};

    public struct Slot has key {
        id: UID,
        keeper: Option<address>,
    }

    public fun current(slot: &Slot): Option<address> {
        slot.keeper
    }
}
