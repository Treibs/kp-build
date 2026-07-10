module race_app::race {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::TxContext;
    use sui::coin::{Self, Coin, SUI};
    use sui::balance::{Self, Balance};
    use sui::table::{Self, Table};
    use std::vector;

    public struct Race has key {
        id: UID,
        organizer: address,
        bib_counter: u64,
        is_open: bool,
        entry_fee: u64,
        pool: Balance<SUI>,
        runners: Table<u64, address>,
        finishers: vector<u64>,
        medals_awarded: bool,
    }

    public struct Medal has key, store {
        id: UID,
        position: u8,
        runner: address,
    }

    public struct AdminCap has key, store {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        transfer::transfer(
            AdminCap { id: object::new(ctx) },
            ctx.sender(),
        );
    }

    public fun create(
        entry_fee: u64,
        ctx: &mut TxContext,
    ) {
        let race = Race {
            id: object::new(ctx),
            organizer: ctx.sender(),
            bib_counter: 0,
            is_open: true,
            entry_fee,
            pool: balance::zero(),
            runners: table::new(ctx),
            finishers: vector[],
            medals_awarded: false,
        };
        transfer::share_object(race);
    }

    public fun register(
        race: &mut Race,
        fee: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        assert!(race.is_open);
        assert!(coin::value(&fee) == race.entry_fee);

        race.bib_counter = race.bib_counter + 1;
        table::add(&mut race.runners, race.bib_counter, ctx.sender());
        balance::join(&mut race.pool, coin::into_balance(fee));
    }

    public fun close(
        race: &mut Race,
        _cap: &AdminCap,
    ) {
        race.is_open = false;
    }

    public fun record_finish(
        race: &mut Race,
        bib: u64,
        _cap: &AdminCap,
    ) {
        assert!(!race.is_open);
        assert!(table::contains(&race.runners, bib));
        vector::push_back(&mut race.finishers, bib);
    }

    public fun award_medals(
        race: &mut Race,
        ctx: &mut TxContext,
    ) {
        assert!(!race.medals_awarded);
        race.medals_awarded = true;

        let len = vector::length(&race.finishers);
        let max = if (len > 3) { 3 } else { len };

        let mut i = 0;
        while (i < max) {
            let bib = *vector::borrow(&race.finishers, i);
            let runner = *table::borrow(&race.runners, bib);

            let medal = Medal {
                id: object::new(ctx),
                position: ((i + 1) as u8),
                runner,
            };

            transfer::public_transfer(medal, runner);
            i = i + 1;
        };
    }

    public fun claim(
        race: &mut Race,
        _cap: &AdminCap,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        assert!(!race.is_open);
        let amount = balance::value(&race.pool);
        let coin_balance = balance::split(&mut race.pool, amount);
        coin::from_balance(coin_balance, ctx)
    }
}
