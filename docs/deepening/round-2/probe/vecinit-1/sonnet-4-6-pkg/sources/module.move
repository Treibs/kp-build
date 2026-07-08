module music::playlist {
    use std::string::String;

    public struct Playlist has key {
        id: UID,
        tracks: vector<String>,
    }

    public fun create(ctx: &mut TxContext) {
        let playlist = Playlist {
            id: object::new(ctx),
            tracks: vector[],
        };
        transfer::transfer(playlist, ctx.sender());
    }

    public fun add(playlist: &mut Playlist, name: String) {
        playlist.tracks.push_back(name);
    }

    public fun remove_at(playlist: &mut Playlist, index: u64) {
        assert!(index < playlist.tracks.length());
        playlist.tracks.remove(index);
    }
}
