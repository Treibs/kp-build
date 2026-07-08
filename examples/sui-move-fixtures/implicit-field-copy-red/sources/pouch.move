module implicit_field_copy_red::pouch {
    // `let gem = p.gem;` is a read of the field, and reading by the dot
    // operator copies — `Gem` has no `copy` ability, so this is rejected
    // (and the never-consumed `p` is a second error downstream).
    public struct Gem has store {}

    public struct Pouch has store {
        gem: Gem,
    }

    public fun take(p: Pouch): Gem {
        let gem = p.gem;
        gem
    }
}
