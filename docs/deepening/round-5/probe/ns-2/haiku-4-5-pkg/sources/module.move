module 0x0::wishlist_board {
    use std::string::String;
    use std::vector;
    use sui::dynamic_field;
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;

    public struct Board has key {
        id: UID,
        readers: vector<address>,
    }

    public struct Wishlist has store {
        titles: vector<String>,
    }

    public fun new(ctx: &mut TxContext): Board {
        Board {
            id: object::new(ctx),
            readers: vector[],
        }
    }

    public fun add_title(board: &mut Board, reader: address, title: String) {
        if (!dynamic_field::exists<address>(&board.id, reader)) {
            vector::push_back(&mut board.readers, reader);
            dynamic_field::add(&mut board.id, reader, Wishlist {
                titles: vector[]
            });
        }
        
        let wishlist = dynamic_field::borrow_mut<address, Wishlist>(&mut board.id, reader);
        vector::push_back(&mut wishlist.titles, title);
    }

    public fun remove_title(board: &mut Board, reader: address, title: String) {
        assert!(dynamic_field::exists<address>(&board.id, reader));
        
        let wishlist = dynamic_field::borrow_mut<address, Wishlist>(&mut board.id, reader);
        let (found, index) = find_title(&wishlist.titles, &title);
        assert!(found);
        vector::remove(&mut wishlist.titles, index);
    }

    public fun get_wishlist_count(board: &Board, reader: address): u64 {
        if (dynamic_field::exists<address>(&board.id, reader)) {
            let wishlist = dynamic_field::borrow<address, Wishlist>(&board.id, reader);
            vector::length(&wishlist.titles)
        } else {
            0
        }
    }

    public fun get_readers_count(board: &Board): u64 {
        vector::length(&board.readers)
    }

    fun find_title(titles: &vector<String>, target: &String): (bool, u64) {
        let i = 0;
        let len = vector::length(titles);
        while (i < len) {
            if (vector::borrow(titles, i) == target) {
                return (true, i)
            };
            i = i + 1;
        };
        (false, 0)
    }
}
