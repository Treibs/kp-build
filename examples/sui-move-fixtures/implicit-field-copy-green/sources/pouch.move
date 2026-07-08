module implicit_field_copy_green::pouch {
    // Moving a non-`copy` field out of a struct: destructure the struct.
    // Field access (`p.gem`) reads by copy and needs the `copy` ability.
    public struct Gem has store {}

    public struct Pouch has store {
        gem: Gem,
    }

    public fun take(p: Pouch): Gem {
        let Pouch { gem } = p;
        gem
    }
}
