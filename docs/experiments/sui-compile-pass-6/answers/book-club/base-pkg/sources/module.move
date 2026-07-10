module book_club::club {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::object::{Self, UID};
    use sui::table::{Self, Table};
    use sui::tx_context::{TxContext, sender};
    use sui::transfer;
    use sui::balance::{Self, Balance};
    use std::string::String;

    struct BookClub has key {
        id: UID,
        pool: Balance<SUI>,
        shelf: vector<Book>,
        epoch_dues: u64,
        members: Table<address, u64>,
    }

    struct LibrarianCap has key {
        id: UID,
    }

    struct Book has store, copy, drop {
        title: String,
        cost: u64,
    }

    public fun create(epoch_dues: u64, ctx: &mut TxContext) {
        let club = BookClub {
            id: object::new(ctx),
            pool: balance::zero(),
            shelf: vector::empty(),
            epoch_dues,
            members: table::new(ctx),
        };
        
        transfer::share_object(club);
        
        let cap = LibrarianCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, sender(ctx));
    }

    public fun join(club: &mut BookClub, payment: Coin<SUI>, ctx: &TxContext) {
        assert!(coin::value(&payment) == club.epoch_dues, 1);
        
        let sender_addr = sender(ctx);
        table::add(&mut club.members, sender_addr, 1);
        
        coin::put(&mut club.pool, payment);
    }

    public fun top_up(club: &mut BookClub, payment: Coin<SUI>, ctx: &TxContext) {
        assert!(coin::value(&payment) == club.epoch_dues, 1);
        
        let sender_addr = sender(ctx);
        let paid_through = table::borrow_mut(&mut club.members, sender_addr);
        *paid_through = *paid_through + 1;
        
        coin::put(&mut club.pool, payment);
    }

    public fun acquire_book(
        _cap: &LibrarianCap,
        club: &mut BookClub,
        title: String,
        cost: u64,
    ) {
        assert!(balance::value(&club.pool) >= cost, 2);
        
        let book = Book { title, cost };
        vector::push_back(&mut club.shelf, book);
        
        let _ = balance::split(&mut club.pool, cost);
    }

    public fun paid_through(club: &BookClub, member: address): u64 {
        *table::borrow(&club.members, member)
    }

    public fun shelf_size(club: &BookClub): u64 {
        vector::length(&club.shelf)
    }

    public fun pool_balance(club: &BookClub): u64 {
        balance::value(&club.pool)
    }
}
