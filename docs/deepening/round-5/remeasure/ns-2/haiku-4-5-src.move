module book_board::board {
    use std::string::String;
    use std::vector;
    use sui::table::{Self, Table};
    use sui::object::{Self, UID};
    use sui::tx_context::{TxContext, sender};
    use sui::transfer;

    public struct Board has key {
        id: UID,
        wishlists: Table<address, vector<String>>,
    }

    fun init(ctx: &mut TxContext) {
        let board = Board {
            id: object::new(ctx),
            wishlists: table::new(ctx),
        };
        transfer::share_object(board);
    }

    public fun add_title(board: &mut Board, title: String, ctx: &TxContext) {
        let reader = sender(ctx);
        if (!table::contains(&board.wishlists, reader)) {
            table::add(&mut board.wishlists, reader, vector[]);
        };
        let wishlist = table::borrow_mut(&mut board.wishlists, reader);
        vector::push_back(wishlist, title);
    }

    public fun remove_title(board: &mut Board, title: String, ctx: &TxContext) {
        let reader = sender(ctx);
        assert!(table::contains(&board.wishlists, reader), 1);
        
        let wishlist = table::borrow_mut(&mut board.wishlists, reader);
        let mut i = 0;
        let len = vector::length(wishlist);
        while (i < len) {
            if (vector::borrow(wishlist, i) == &title) {
                vector::remove(wishlist, i);
                return
            };
            i = i + 1;
        };
        assert!(false, 2);
    }

    public fun reader_title_count(board: &Board, reader: address): u64 {
        if (!table::contains(&board.wishlists, reader)) {
            0
        } else {
            vector::length(table::borrow(&board.wishlists, reader))
        }
    }

    public fun reader_count(board: &Board): u64 {
        table::length(&board.wishlists)
    }
}
