module profile::profile;

use std::string::{Self, String};
use sui::dynamic_field;

const ENoBio: u64 = 0;

public struct Profile has key {
    id: UID,
}

public fun set_bio(profile: &mut Profile, bio: String) {
    if (dynamic_field::exists(&profile.id, b"bio")) {
        let _ = dynamic_field::remove(&profile.id, b"bio");
    };
    dynamic_field::add(&mut profile.id, b"bio", bio);
}

public fun clear_bio(profile: &mut Profile): String {
    assert!(dynamic_field::exists(&profile.id, b"bio"), ENoBio);
    dynamic_field::remove(&profile.id, b"bio")
}

public fun get_bio(profile: &Profile): String {
    if (dynamic_field::exists(&profile.id, b"bio")) {
        *dynamic_field::borrow(&profile.id, b"bio")
    } else {
        string::utf8(b"")
    }
}
