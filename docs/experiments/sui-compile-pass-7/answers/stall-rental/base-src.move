module farmers_market::stall_board {
    use sui::object::{Self, UID};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::balance::{Self, Balance};
    use std::vector;

    public struct InspectorCap has key {
        id: UID,
    }

    public struct RentedStall has store {
        number: u64,
        vendor: address,
        deposit: u64,
    }

    public struct MarketBoard has key {
        id: UID,
        rented: vector<RentedStall>,
        pool: Balance<SUI>,
    }

    fun init(ctx: &mut TxContext) {
        transfer::share_object(MarketBoard {
            id: object::new(ctx),
            rented: vector::empty(),
            pool: balance::zero(),
        });
        
        transfer::transfer(
            InspectorCap { id: object::new(ctx) },
            tx_context::sender(ctx),
        );
    }

    public fun rent_stall(
        board: &mut MarketBoard,
        stall_num: u64,
        rent_coin: Coin<SUI>,
        deposit_coin: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let vendor = tx_context::sender(ctx);
        let deposit_amount = coin::value(&deposit_coin);

        balance::join(&mut board.pool, coin::into_balance(rent_coin));
        balance::join(&mut board.pool, coin::into_balance(deposit_coin));

        vector::push_back(&mut board.rented, RentedStall {
            number: stall_num,
            vendor,
            deposit: deposit_amount,
        });
    }

    public fun mark_clean(
        _inspector: &InspectorCap,
        board: &mut MarketBoard,
        index: u64,
        ctx: &mut TxContext,
    ) {
        let stall = vector::remove(&mut board.rented, index);
        let RentedStall { vendor, deposit, .. } = stall;

        let returned = coin::from_balance(
            balance::split(&mut board.pool, deposit),
            ctx,
        );
        transfer::public_transfer(returned, vendor);
    }

    public fun mark_dirty(
        _inspector: &InspectorCap,
        board: &mut MarketBoard,
        index: u64,
    ) {
        let stall = vector::remove(&mut board.rented, index);
        let _ = stall;
    }

    public fun stalls_today(board: &MarketBoard): vector<(u64, address)> {
        let mut result = vector::empty();
        let mut i = 0;
        let len = vector::length(&board.rented);
        while (i < len) {
            let s = vector::borrow(&board.rented, i);
            vector::push_back(&mut result, (s.number, s.vendor));
            i = i + 1;
        };
        result
    }

    public fun pool_total(board: &MarketBoard): u64 {
        balance::value(&board.pool)
    }
}
