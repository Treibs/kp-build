module key_field_store_green::board {
    use std::string::String;

    // Every field of a `key` struct must have `store` — including the
    // element type of a vector field.
    public struct Post has store {
        text: String,
    }

    public struct Board has key {
        id: UID,
        posts: vector<Post>,
    }

    public fun post(board: &mut Board, text: String) {
        board.posts.push_back(Post { text });
    }
}
