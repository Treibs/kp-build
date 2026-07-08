Write a Sui Move module `profile::profile` (edition 2024). A `Profile` object stores an OPTIONAL
bio as a dynamic field on its own `id` (key: the byte string b"bio", value: `std::string::String`).
Provide: `set_bio(profile, bio)` which replaces any existing bio (check existence first),
`clear_bio(profile): String` which removes and returns the stored bio (abort with a named constant
if none), and `get_bio(profile): String` returning a copy of the bio or an empty string if unset.
