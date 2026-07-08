module destructure_ignore_green::crate_mod {
    // Dismantling an object: bind the non-`drop` field (`id: UID`) and
    // consume it explicitly with `object::delete`.
    public struct Crate has key {
        id: UID,
    }

    public fun open(c: Crate) {
        let Crate { id } = c;
        object::delete(id);
    }
}
