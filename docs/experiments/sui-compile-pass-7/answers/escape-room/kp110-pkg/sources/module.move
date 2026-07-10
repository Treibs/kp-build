module escape_room::booking {
    use sui::coin::{Self, Coin, SUI};
    use sui::table::{Self, Table};
    use sui::clock::Clock;
    use std::string::String;
    use sui::event;

    public struct Room has key {
        id: UID,
        name: String,
        target_time_ms: u64,
        bookings: Table<u64, Booking>,
    }

    public struct Booking has store {
        team_name: String,
        booker_address: address,
        scheduled_epoch: u64,
        booking_time: u64,
        fee: u64,
        status: u8,
    }

    public struct Pool has key {
        id: UID,
        balance: Coin<SUI>,
    }

    public struct BookingCreated has copy, drop {
        room_name: String,
        team_name: String,
        fee: u64,
    }

    public struct FinishRecorded has copy, drop {
        room_name: String,
        team_name: String,
        refund_amount: u64,
    }

    fun init(ctx: &mut TxContext) {
        let pool = Pool {
            id: object::new(ctx),
            balance: coin::zero(ctx),
        };
        transfer::share_object(pool);
    }

    public fun create_room(
        name: String,
        target_time_ms: u64,
        ctx: &mut TxContext,
    ) {
        let room = Room {
            id: object::new(ctx),
            name,
            target_time_ms,
            bookings: table::new(ctx),
        };
        transfer::share_object(room);
    }

    public fun book_room(
        room: &mut Room,
        pool: &mut Pool,
        team_name: String,
        scheduled_epoch: u64,
        fee: Coin<SUI>,
        clock: &Clock,
        ctx: &mut TxContext,
    ) {
        let fee_amount = coin::value(&fee);
        coin::join(&mut pool.balance, fee);

        let booking_time = clock.timestamp_ms();

        let booking = Booking {
            team_name,
            booker_address: ctx.sender(),
            scheduled_epoch,
            booking_time,
            fee: fee_amount,
            status: 0,
        };

        table::add(&mut room.bookings, scheduled_epoch, booking);

        event::emit(BookingCreated {
            room_name: room.name,
            team_name,
            fee: fee_amount,
        });
    }

    public fun record_finish(
        room: &mut Room,
        pool: &mut Pool,
        scheduled_epoch: u64,
        finish_time: u64,
        ctx: &mut TxContext,
    ) {
        let booking = table::borrow_mut(&mut room.bookings, scheduled_epoch);

        let refund = if (finish_time <= room.target_time_ms) {
            booking.status = 1;
            booking.fee / 2
        } else {
            booking.status = 2;
            0
        };

        if (refund > 0) {
            let refund_coin = coin::split(&mut pool.balance, refund, ctx);
            transfer::public_transfer(refund_coin, booking.booker_address);
        };

        event::emit(FinishRecorded {
            room_name: room.name,
            team_name: booking.team_name,
            refund_amount: refund,
        });
    }

    public fun finalize_expired(
        room: &mut Room,
        scheduled_epoch: u64,
        clock: &Clock,
    ) {
        let current_time = clock.timestamp_ms();
        assert!(current_time > scheduled_epoch, 0);

        let booking = table::borrow_mut(&mut room.bookings, scheduled_epoch);
        assert!(booking.status == 0, 0);

        booking.status = 3;
    }

    public fun get_room_bookings(room: &Room): &Table<u64, Booking> {
        &room.bookings
    }

    public fun get_pool_total(pool: &Pool): u64 {
        coin::value(&pool.balance)
    }
}
