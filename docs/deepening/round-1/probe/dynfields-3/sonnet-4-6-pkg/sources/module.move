module profile::profile;

use sui::dynamic_field;
use std::string::String;

const ENO_BIO: u64 = 0;

public struct Profile has key {
    id: UID,
}

public fun new(ctx: &mut TxContext): Profile {
    Profile { id: object::new(ctx) }
}

public fun set_bio(profile: &mut Profile, bio: String) {
    let key = b"bio";
    if (dynamic_field::exists_(&profile.id, key)) {
        let existing: &mut String = dynamic_field::borrow_mut(&mut profile.id, key);
        *existing = bio;
    } else {
        dynamic_field::add(&mut profile.id, key, bio);
    }
}

public fun clear_bio(profile: &mut Profile): String {
    assert!(dynamic_field::exists_(&profile.id, b"bio"), ENO_BIO);
    dynamic_field::remove(&mut profile.id, b"bio")
}

public fun get_bio(profile: &Profile): String {
    let key = b"bio";
    if (dynamic_field::exists_(&profile.id, key)) {
        *dynamic_field::borrow(&profile.id, key)
    } else {
        std::string::utf8(b"")
    }
}
