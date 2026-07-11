module campground::booking {
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::table::{Self, Table};
    use sui::transfer;

    public struct Campground has key, store {
        id: UID,
        nightly_rate: u64,
        till: Balance<SUI>,
        bookings: Table<u64, Booking>,
    }

    public struct Booking has store {
        site_id: u64,
        camper: address,
        nights_booked: u64,
        nights_remaining: u64,
    }

    public struct AdminCap has key, store {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        let admin_cap = AdminCap {
            id: object::new(ctx),
        };
        transfer::transfer(admin_cap, ctx.sender());

        let campground = Campground {
            id: object::new(ctx),
            nightly_rate: 100,
            till: balance::zero(),
            bookings: table::new(ctx),
        };
        transfer::share_object(campground);
    }

    public fun set_nightly_rate(_cap: &AdminCap, campground: &mut Campground, rate: u64) {
        campground.nightly_rate = rate;
    }

    public fun book_site(
        _cap: &AdminCap,
        campground: &mut Campground,
        site_id: u64,
        camper: address,
        nights: u64,
        payment: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let cost = campground.nightly_rate * nights;
        let coin_value = coin::value(&payment);
        assert!(coin_value >= cost, 0);

        balance::join(&mut campground.till, coin::into_balance(payment));

        let booking = Booking {
            site_id,
            camper,
            nights_booked: nights,
            nights_remaining: nights,
        };

        table::add(&mut campground.bookings, site_id, booking);
    }

    public fun check_out_early(
        campground: &mut Campground,
        site_id: u64,
        ctx: &mut TxContext,
    ) {
        assert!(table::contains(&campground.bookings, site_id), 1);

        let booking = table::remove(&mut campground.bookings, site_id);
        let refund_nights = booking.nights_remaining;
        let refund_amount = campground.nightly_rate * refund_nights;

        let refund = coin::from_balance(
            balance::split(&mut campground.till, refund_amount),
            ctx,
        );
        transfer::public_transfer(refund, booking.camper);

        let Booking { site_id: _, camper: _, nights_booked: _, nights_remaining: _ } = booking;
    }

    public fun nights_remaining(campground: &Campground, site_id: u64): u64 {
        if (table::contains(&campground.bookings, site_id)) {
            table::borrow(&campground.bookings, site_id).nights_remaining
        } else {
            0
        }
    }

    public fun occupied_sites(campground: &Campground): u64 {
        table::length(&campground.bookings)
    }
}
