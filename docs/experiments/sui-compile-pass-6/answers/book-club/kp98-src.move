module book_club::club {
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::table::{Self, Table};
    use std::string::String;
    use std::vector;

    public struct Club has key {
        id: UID,
        librarian: address,
        pool: Balance<SUI>,
        current_epoch: u64,
        shelf: vector<Book>,
        members: Table<address, u64>,
        epoch_dues: u64,
    }

    public struct Book has copy, drop, store {
        title: String,
        cost: u64,
    }

    public struct LibrarianCap has key, store {
        id: UID,
    }

    public fun create_club(epoch_dues: u64, ctx: &mut TxContext) {
        let librarian = tx_context::sender(ctx);
        
        let club = Club {
            id: object::new(ctx),
            librarian,
            pool: balance::zero(),
            current_epoch: 1,
            shelf: vector[],
            members: table::new(ctx),
            epoch_dues,
        };
        
        let cap = LibrarianCap {
            id: object::new(ctx),
        };
        
        transfer::share_object(club);
        transfer::transfer(cap, librarian);
    }

    public fun pay_dues(club: &mut Club, payment: Coin<SUI>, ctx: &mut TxContext) {
        let amount = coin::value(&payment);
        assert!(amount >= club.epoch_dues, 0);
        
        balance::join(&mut club.pool, coin::into_balance(payment));
        
        let member = tx_context::sender(ctx);
        if (table::contains(&club.members, member)) {
            let paid_through = table::borrow_mut(&mut club.members, member);
            *paid_through = club.current_epoch;
        } else {
            table::add(&mut club.members, member, club.current_epoch);
        };
    }

    public fun acquire_book(
        club: &mut Club,
        _cap: &LibrarianCap,
        title: String,
        cost: u64,
    ) {
        assert!(balance::value(&club.pool) >= cost, 1);
        
        let _balance = balance::split(&mut club.pool, cost);
        let book = Book { title, cost };
        vector::push_back(&mut club.shelf, book);
    }

    public fun member_paid_through(club: &Club, member: address): u64 {
        if (table::contains(&club.members, member)) {
            *table::borrow(&club.members, member)
        } else {
            0
        }
    }

    public fun shelf_size(club: &Club): u64 {
        vector::length(&club.shelf)
    }

    public fun pool_balance(club: &Club): u64 {
        balance::value(&club.pool)
    }
}
