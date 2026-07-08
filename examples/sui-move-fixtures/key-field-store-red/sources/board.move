module key_field_store_red::board {
    use std::string::String;

    // Missing `store`: a plain struct cannot be a field of a `key` object.
    public struct Post {
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
