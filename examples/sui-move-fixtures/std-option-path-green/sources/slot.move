module std_option_path_green::slot {
    // Option<T> is std::option — implicitly imported in edition 2024;
    // no use line is needed (and any explicit path is std::, never sui::)
    public struct Slot has key {
        id: UID,
        keeper: Option<address>,
    }

    public fun current(slot: &Slot): Option<address> {
        slot.keeper
    }

    public fun vacate(slot: &mut Slot): Option<address> {
        let previous = slot.keeper;
        slot.keeper = option::none();
        previous
    }
}
