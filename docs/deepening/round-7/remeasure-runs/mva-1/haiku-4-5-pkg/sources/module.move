module ski_valet::desk {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};
    use sui::table::{Self, Table};

    public struct Ski has key, store {
        id: UID,
        owner: address,
        deposit_amount: u64,
    }

    public struct SkiValet has key {
        id: UID,
        skis: Table<address, Ski>,
        earnings: Balance<SUI>,
    }

    fun init(ctx: &mut TxContext) {
        let valet = SkiValet {
            id: object::new(ctx),
            skis: table::new(ctx),
            earnings: balance::zero(),
        };
        transfer::share_object(valet);
    }

    public fun check_in(
        valet: &mut SkiValet,
        deposit: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let owner = tx_context::sender(ctx);
        let deposit_amount = coin::value(&deposit);
        
        let ski = Ski {
            id: object::new(ctx),
            owner,
            deposit_amount,
        };
        
        coin::put(&mut valet.earnings, deposit);
        table::add(&mut valet.skis, owner, ski);
    }

    public fun pickup(
        valet: &mut SkiValet,
        storage_fee: u64,
        ctx: &mut TxContext,
    ) {
        let owner = tx_context::sender(ctx);
        let ski = table::remove(&mut valet.skis, owner);
        
        let refund_amount = ski.deposit_amount - storage_fee;
        let refund_coin = coin::take(&mut valet.earnings, refund_amount, ctx);
        
        transfer::public_transfer(ski, owner);
        transfer::public_transfer(refund_coin, owner);
    }

    public fun earnings(valet: &SkiValet): u64 {
        balance::value(&valet.earnings)
    }

    public fun stored_count(valet: &SkiValet): u64 {
        table::length(&valet.skis)
    }
}
