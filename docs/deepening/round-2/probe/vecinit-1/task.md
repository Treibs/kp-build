Write a Sui Move module `music::playlist` (edition 2024). A `Playlist` object holds an ordered
list of track names (`std::string::String`). Provide functions to create an empty playlist for
the sender, `add(playlist, name)` to append a track, and `remove_at(playlist, index)` to remove
the track at a position (abort if out of bounds), preserving the order of the rest.
