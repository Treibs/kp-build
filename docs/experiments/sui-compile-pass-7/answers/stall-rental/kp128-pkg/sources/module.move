module farmers_market::market {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};
    use sui::event;
    use sui::option::{Self, Option};

    const EStallNotFound: u64 = 1;
    const ENotRenter: u64 = 2;
    const ENotClean: u64 = 3;

    public struct Market has key {
        id: UID,
        stalls: vector<Stall>,
        pool: Balance<SUI>,
    }

    public struct Stall has store {
        number: u64,
        renter: address,
        deposit_amount: u64,
        is_clean: Option<bool>,
    }

    public struct InspectorCap has key, store {
        id: UID,
    }

    public struct StallRented has copy, drop {
        stall_number: u64,
        renter: address,
    }

    public struct StallMarked has copy, drop {
        stall_number: u64,
        is_clean: bool,
    }

    public struct DepositClaimed has copy, drop {
        stall_number: u64,
        renter: address,
        amount: u64,
    }

    fun init(ctx: &mut TxContext) {
        let market = Market {
            id: object::new(ctx),
            stalls: vector[],
            pool: balance::zero(),
        };
        transfer::share_object(market);

        let inspector_cap = InspectorCap {
            id: object::new(ctx),
        };
        transfer::transfer(inspector_cap, ctx.sender());
    }

    public fun rent_stall(
        market: &mut Market,
        stall_number: u64,
        rent: Coin<SUI>,
        deposit: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let deposit_amount = coin::value(&deposit);

        let mut pool_coins = coin::into_balance(rent);
        balance::join(&mut pool_coins, coin::into_balance(deposit));
        balance::join(&mut market.pool, pool_coins);

        let stall = Stall {
            number: stall_number,
            renter: ctx.sender(),
            deposit_amount,
            is_clean: option::none(),
        };

        vector::push_back(&mut market.stalls, stall);

        event::emit(StallRented {
            stall_number,
            renter: ctx.sender(),
        });
    }

    public fun mark_stall_clean(
        _cap: &InspectorCap,
        market: &mut Market,
        stall_number: u64,
    ) {
        let mut i = 0;
        let len = vector::length(&market.stalls);
        while (i < len) {
            let stall = vector::borrow_mut(&mut market.stalls, i);
            if (stall.number == stall_number) {
                stall.is_clean = option::some(true);
                event::emit(StallMarked {
                    stall_number,
                    is_clean: true,
                });
                return;
            };
            i = i + 1;
        };
        abort EStallNotFound;
    }

    public fun mark_stall_dirty(
        _cap: &InspectorCap,
        market: &mut Market,
        stall_number: u64,
    ) {
        let mut i = 0;
        let len = vector::length(&market.stalls);
        while (i < len) {
            let stall = vector::borrow_mut(&mut market.stalls, i);
            if (stall.number == stall_number) {
                stall.is_clean = option::some(false);
                event::emit(StallMarked {
                    stall_number,
                    is_clean: false,
                });
                return;
            };
            i = i + 1;
        };
        abort EStallNotFound;
    }

    public fun claim_deposit(
        market: &mut Market,
        stall_number: u64,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let mut i = 0;
        let len = vector::length(&market.stalls);
        while (i < len) {
            let stall = vector::borrow(&market.stalls, i);
            if (stall.number == stall_number) {
                assert!(stall.renter == ctx.sender(), ENotRenter);
                assert!(*option::borrow(&stall.is_clean), ENotClean);

                let deposit_amount = stall.deposit_amount;

                let Stall {
                    number: _,
                    renter: _,
                    deposit_amount: _,
                    is_clean: _,
                } = vector::remove(&mut market.stalls, i);

                let withdrawn = balance::split(&mut market.pool, deposit_amount);
                let coin = coin::from_balance(withdrawn, ctx);

                event::emit(DepositClaimed {
                    stall_number,
                    renter: ctx.sender(),
                    amount: deposit_amount,
                });

                return coin;
            };
            i = i + 1;
        };
        abort EStallNotFound;
    }

    public fun stalls_rented_today(market: &Market): vector<u64> {
        let mut result = vector[];
        let mut i = 0;
        while (i < vector::length(&market.stalls)) {
            let stall = vector::borrow(&market.stalls, i);
            vector::push_back(&mut result, stall.number);
            i = i + 1;
        };
        result
    }

    public fun pool_total(market: &Market): u64 {
        balance::value(&market.pool)
    }
}
