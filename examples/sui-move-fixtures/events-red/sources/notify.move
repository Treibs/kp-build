module events_red::notify {
    use sui::event;

    // Missing `copy`: `event::emit<T: copy + drop>` will reject this.
    public struct ValueSet has drop {
        value: u64,
    }

    public fun set(value: u64) {
        event::emit(ValueSet { value });
    }
}
