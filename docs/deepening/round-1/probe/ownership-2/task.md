Write a Sui Move module `board::board` (edition 2024). A `Board` object must be created AND shared
in the same function. Anyone may call the entry function `post(board: &mut Board, text: vector<u8>)`
appending a `Post` (a plain struct value stored in a `vector<Post>` field). The creator of the
board receives an owned `ModCap` at creation; `remove_post(cap: &ModCap, board: &mut Board, i: u64)`
deletes a post by index and must only work for the matching board (bind the cap to the board's id).
