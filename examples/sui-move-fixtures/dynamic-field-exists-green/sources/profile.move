module dynamic_field_exists_green::profile {
    use std::string::String;
    use sui::dynamic_field;

    public struct Profile has key {
        id: UID,
    }

    public fun set_bio(profile: &mut Profile, bio: String) {
        // `exists` is the current name on sui 1.74.1 (`exists_` is deprecated).
        if (dynamic_field::exists(&profile.id, b"bio")) {
            let _old: String = dynamic_field::remove(&mut profile.id, b"bio");
        };
        dynamic_field::add(&mut profile.id, b"bio", bio);
    }
}
