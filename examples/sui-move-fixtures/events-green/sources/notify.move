module events_green::notify {
    use sui::event;

    public struct ValueSet has copy, drop {
        value: u64,
    }

    public fun set(value: u64) {
        event::emit(ValueSet { value });
    }
}
