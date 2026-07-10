module reference_type_argument_red::door {
    // references are not first-class types: they cannot be type
    // arguments — pass Option<ID> or borrow at use (see green)
    public struct Stamp has key {
        id: UID,
    }

    public fun admit(stamp: Option<&Stamp>): bool {
        option::is_some(&stamp)
    }
}
