module carpool::ledger {
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;
    use sui::coin::{Coin, from_balance};
    use sui::sui::SUI;
    use sui::transfer;
    use sui::balance::{Self, Balance};
    use std::vector;
    use std::option::{Self, Option};

    public struct Ledger has key {
        id: UID,
        rides: vector<Ride>,
        pool: Balance<SUI>,
        current_epoch: u64,
    }

    public struct Ride has store {
        driver: address,
        epoch: u64,
    }

    fun init(ctx: &mut TxContext) {
        let ledger = Ledger {
            id: object::new(ctx),
            rides: vector[],
            pool: balance::zero(),
            current_epoch: 1,
        };
        transfer::share_object(ledger);
    }

    public fun log_ride(
        ledger: &mut Ledger,
        mut payments: vector<Coin<SUI>>,
        ctx: &mut TxContext,
    ) {
        let sender = ctx.sender();

        while (vector::length(&payments) > 0) {
            let payment = vector::pop_back(&mut payments);
            balance::join(&mut ledger.pool, from_balance(payment, ctx));
        };

        let ride = Ride {
            driver: sender,
            epoch: ledger.current_epoch,
        };
        vector::push_back(&mut ledger.rides, ride);
    }

    public fun rides_in_epoch(ledger: &Ledger, member: address, epoch: u64): u64 {
        let mut count: u64 = 0;
        let mut i = 0;
        while (i < vector::length(&ledger.rides)) {
            let ride = vector::borrow(&ledger.rides, i);
            if (ride.driver == member && ride.epoch == epoch) {
                count = count + 1;
            };
            i = i + 1;
        };
        count
    }

    public fun monthly_winner(ledger: &Ledger, epoch: u64): Option<address> {
        let mut max_rides: u64 = 0;
        let mut winner: Option<address> = option::none();
        let mut checked: vector<address> = vector[];

        let mut i = 0;
        while (i < vector::length(&ledger.rides)) {
            let ride = vector::borrow(&ledger.rides, i);
            if (ride.epoch == epoch) {
                let mut is_checked = false;
                let mut j = 0;
                while (j < vector::length(&checked)) {
                    if (*vector::borrow(&checked, j) == ride.driver) {
                        is_checked = true;
                    };
                    j = j + 1;
                };

                if (!is_checked) {
                    vector::push_back(&mut checked, ride.driver);
                    let count = rides_in_epoch(ledger, ride.driver, epoch);
                    if (count > max_rides) {
                        max_rides = count;
                        winner = option::some(ride.driver);
                    };
                };
            };
            i = i + 1;
        };
        winner
    }

    public fun pool_balance(ledger: &Ledger): u64 {
        balance::value(&ledger.pool)
    }

    public fun advance_epoch(ledger: &mut Ledger) {
        ledger.current_epoch = ledger.current_epoch + 1;
    }

    public fun payout_winner(
        ledger: &mut Ledger,
        winner: address,
        ctx: &mut TxContext,
    ) {
        let amount = balance::value(&ledger.pool);
        let payout = from_balance(balance::split(&mut ledger.pool, amount), ctx);
        transfer::public_transfer(payout, winner);
    }
}
