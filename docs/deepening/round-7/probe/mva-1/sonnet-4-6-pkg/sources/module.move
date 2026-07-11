module ski_valet::desk {
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};
    use sui::sui::SUI;
    use sui::object_table::{Self, ObjectTable};

    public struct ValetDesk has key {
        id: UID,
        storage_fee: u64,
        earnings: Balance<SUI>,
        pairs: ObjectTable<ID, SkiPair>,
    }

    public struct ValetCap has key, store {
        id: UID,
    }

    public struct SkiPair has key, store {
        id: UID,
        owner: address,
        deposit: Balance<SUI>,
    }

    fun init(ctx: &mut TxContext) {
        let cap = ValetCap { id: object::new(ctx) };
        let desk = ValetDesk {
            id: object::new(ctx),
            storage_fee: 1_000_000_000,
            earnings: balance::zero(),
            pairs: object_table::new(ctx),
        };
        transfer::share_object(desk);
        transfer::transfer(cap, ctx.sender());
    }

    public fun check_in(desk: &mut ValetDesk, payment: Coin<SUI>, ctx: &mut TxContext) {
        let uid = object::new(ctx);
        let pair_id = object::uid_to_inner(&uid);
        let pair = SkiPair {
            id: uid,
            owner: ctx.sender(),
            deposit: coin::into_balance(payment),
        };
        object_table::add(&mut desk.pairs, pair_id, pair);
    }

    public fun pick_up(_cap: &ValetCap, desk: &mut ValetDesk, pair_id: ID, ctx: &mut TxContext) {
        let mut pair = object_table::remove(&mut desk.pairs, pair_id);
        let fee = desk.storage_fee;
        assert!(balance::value(&pair.deposit) >= fee, 0);
        let fee_balance = balance::split(&mut pair.deposit, fee);
        balance::join(&mut desk.earnings, fee_balance);
        let SkiPair { id, owner, deposit } = pair;
        object::delete(id);
        let refund = coin::from_balance(deposit, ctx);
        transfer::public_transfer(refund, owner);
    }

    public fun set_fee(_cap: &ValetCap, desk: &mut ValetDesk, new_fee: u64) {
        desk.storage_fee = new_fee;
    }

    public fun earnings(desk: &ValetDesk): u64 {
        balance::value(&desk.earnings)
    }

    public fun pairs_stored(desk: &ValetDesk): u64 {
        object_table::length(&desk.pairs)
    }

    public fun storage_fee(desk: &ValetDesk): u64 {
        desk.storage_fee
    }
}
