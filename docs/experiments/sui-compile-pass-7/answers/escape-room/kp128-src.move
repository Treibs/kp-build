module escape_room::booking {
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use std::string::String;
    use std::option::{Self, Option};
    use sui::event;

    const E_BOOKING_NOT_FOUND: u64 = 1;
    const E_ALREADY_FINISHED: u64 = 2;
    const E_INVALID_TIME: u64 = 3;

    public struct AdminCap has key, store {
        id: UID,
    }

    public struct Room has key {
        id: UID,
        name: String,
        target_time_ms: u64,
        pool: Balance<SUI>,
        bookings: vector<Booking>,
    }

    public struct Booking has drop, store {
        id: u64,
        team_name: String,
        booked_epoch_ms: u64,
        finish_time_ms: Option<u64>,
        fee_paid: u64,
    }

    public struct BookingMade has copy, drop {
        room_id: ID,
        booking_id: u64,
    }

    public struct GameFinished has copy, drop {
        room_id: ID,
        booking_id: u64,
        refunded: u64,
    }

    fun init(ctx: &mut TxContext) {
        transfer::transfer(
            AdminCap { id: object::new(ctx) },
            ctx.sender()
        );
    }

    public fun create_room(
        _cap: &AdminCap,
        name: String,
        target_time_ms: u64,
        ctx: &mut TxContext,
    ): Room {
        Room {
            id: object::new(ctx),
            name,
            target_time_ms,
            pool: balance::zero(),
            bookings: vector[],
        }
    }

    public fun book_room(
        room: &mut Room,
        team_name: String,
        booked_epoch_ms: u64,
        payment: Coin<SUI>,
    ) {
        let fee = coin::value(&payment);
        balance::join(&mut room.pool, coin::into_balance(payment));
        
        let booking_id = vector::length(&room.bookings);
        vector::push_back(&mut room.bookings, Booking {
            id: booking_id,
            team_name,
            booked_epoch_ms,
            finish_time_ms: option::none(),
            fee_paid: fee,
        });

        event::emit(BookingMade {
            room_id: object::uid_to_inner(&room.id),
            booking_id,
        });
    }

    public fun record_finish(
        room: &mut Room,
        _cap: &AdminCap,
        booking_id: u64,
        finish_time_ms: u64,
        recipient: address,
        ctx: &mut TxContext,
    ) {
        assert!(booking_id < vector::length(&room.bookings), E_BOOKING_NOT_FOUND);
        
        let booking = vector::borrow_mut(&mut room.bookings, booking_id);
        assert!(option::is_none(&booking.finish_time_ms), E_ALREADY_FINISHED);
        assert!(finish_time_ms >= booking.booked_epoch_ms, E_INVALID_TIME);
        
        let duration = finish_time_ms - booking.booked_epoch_ms;
        let refund = if (duration <= room.target_time_ms) {
            booking.fee_paid / 2
        } else {
            0
        };

        booking.finish_time_ms = option::some(finish_time_ms);

        if (refund > 0) {
            let refund_coin = coin::from_balance(
                balance::split(&mut room.pool, refund),
                ctx
            );
            transfer::public_transfer(refund_coin, recipient);
        };

        event::emit(GameFinished {
            room_id: object::uid_to_inner(&room.id),
            booking_id,
            refunded: refund,
        });
    }

    public fun pool_balance(room: &Room): u64 {
        balance::value(&room.pool)
    }

    public fun view_bookings(room: &Room): &vector<Booking> {
        &room.bookings
    }
}
