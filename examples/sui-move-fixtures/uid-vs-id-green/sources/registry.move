module uid_vs_id_green::registry {
    // the copyable identity of an object is object::id(&obj) (needs
    // T: key) or uid_to_inner on its &UID — never object::id on the UID
    public struct Pet has key {
        id: UID,
    }

    public fun identities(pet: &Pet): (ID, ID) {
        (object::id(pet), object::uid_to_inner(&pet.id))
    }
}
