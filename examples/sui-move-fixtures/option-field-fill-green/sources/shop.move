module option_field_fill_green::shop {
    // `Item` deliberately has `store` but NOT `drop`.
    public struct Item has store { value: u64 }

    public fun value(item: &Item): u64 {
        item.value
    }

    public struct Slot has store { item: std::option::Option<Item> }

    // `option::fill` sets an empty Option in place (aborts if already
    // occupied) — no old value is discarded, so `Item` needs no `drop`.
    public fun stock(slot: &mut Slot, item: Item) {
        slot.item.fill(item);
    }
}
