module option_field_fill_red::shop {
    // `Item` deliberately has `store` but NOT `drop`.
    public struct Item has store { value: u64 }

    public fun value(item: &Item): u64 {
        item.value
    }

    public struct Slot has store { item: std::option::Option<Item> }

    // Assignment overwrites the field, discarding the old Option value —
    // that requires `drop` on the value type, which `Item` lacks.
    public fun stock(slot: &mut Slot, item: Item) {
        slot.item = option::some(item);
    }
}
