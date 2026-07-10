module bookclub::club {
    use std::string::String;
    use std::table::{Table, Self};
    use std::vector;
    use sui::coin::{Coin, SUI};
    use sui::balance::{Balance, Self};
    use sui::tx_context;

    public struct BookClub has key, store {
        id: UID,
        pool: Balance<SUI>,
        shelf: vector<Book>,
        members: Table<address, u64>,
        dues_per_epoch: u64,
        current_epoch: u64,
    }

    public struct Book has copy, drop, store {
        title: String,
        cost: u64,
    }

    public struct LibrarianCap has key, store {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        let club = BookClub {
            id: object::new(ctx),
            pool: balance::zero(),
            shelf: vector[],
            members: table::new(ctx),
            dues_per_epoch: 1_000_000_000,
            current_epoch: 0,
        };
        
        let cap = LibrarianCap {
            id: object::new(ctx),
        };

        transfer::share_object(club);
        transfer::transfer(cap, ctx.sender());
    }

    public fun join(club: &mut BookClub, payment: Coin<SUI>, ctx: &mut TxContext) {
        let member = ctx.sender();
        let amount = coin::value(&payment);
        
        assert!(amount >= club.dues_per_epoch, 0);
        
        let epochs_paid = amount / club.dues_per_epoch;
        let paid_through = club.current_epoch + epochs_paid;
        
        table::add(&mut club.members, member, paid_through);
        balance::join(&mut club.pool, coin::into_balance(payment));
    }

    public fun top_up(club: &mut BookClub, payment: Coin<SUI>, ctx: &mut TxContext) {
        let member = ctx.sender();
        let amount = coin::value(&payment);
        
        let current_paid = *table::borrow(&club.members, member);
        let epochs_paid = amount / club.dues_per_epoch;
        
        let new_epoch = current_paid + epochs_paid;
        table::remove(&mut club.members, member);
        table::add(&mut club.members, member, new_epoch);
        
        balance::join(&mut club.pool, coin::into_balance(payment));
    }

    public fun buy_book(
        club: &mut BookClub,
        _cap: &LibrarianCap,
        title: String,
        cost: u64,
    ) {
        let _book_balance = balance::split(&mut club.pool, cost);
        vector::push_back(&mut club.shelf, Book { title, cost });
    }

    public fun advance_epoch(club: &mut BookClub, _cap: &LibrarianCap) {
        club.current_epoch = club.current_epoch + 1;
    }

    public fun member_epoch(club: &BookClub, member: address): u64 {
        *table::borrow(&club.members, member)
    }

    public fun shelf_size(club: &BookClub): u64 {
        vector::length(&club.shelf)
    }

    public fun pool_balance(club: &BookClub): u64 {
        balance::value(&club.pool)
    }
}
