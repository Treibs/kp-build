module uid_vs_id_red::registry {
    // object::id takes &T where T: key; a raw UID is not an object
    public struct Pet has key {
        id: UID,
    }

    public fun identity(pet: &Pet): ID {
        object::id(&pet.id)
    }
}
