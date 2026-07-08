module board::board {
    use sui::object::ID;

    public struct Post has store {
        text: vector<u8>,
    }

    public struct Board has key {
        id: UID,
        posts: vector<Post>,
    }

    public struct ModCap has key {
        id: UID,
        board_id: ID,
    }

    public fun create(ctx: &mut TxContext) {
        let board = Board {
            id: object::new(ctx),
            posts: vector::empty(),
        };
        let board_id = object::id(&board);
        let cap = ModCap {
            id: object::new(ctx),
            board_id,
        };
        transfer::share_object(board);
        transfer::transfer(cap, ctx.sender());
    }

    public fun post(board: &mut Board, text: vector<u8>) {
        board.posts.push_back(Post { text });
    }

    public fun remove_post(cap: &ModCap, board: &mut Board, i: u64) {
        assert!(cap.board_id == object::id(board));
        let _ = board.posts.remove(i);
    }
}
