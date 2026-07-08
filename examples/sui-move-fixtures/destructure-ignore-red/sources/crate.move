module destructure_ignore_red::crate_mod {
    // Rust's `_` drops any value; Move's `field: _` in a destructure is an
    // ignore, and ignoring is gated on the `drop` ability. `UID` has no
    // `drop`, so `id: _` cannot discard it.
    public struct Crate has key {
        id: UID,
    }

    public fun open(c: Crate) {
        let Crate { id: _ } = c;
    }
}
