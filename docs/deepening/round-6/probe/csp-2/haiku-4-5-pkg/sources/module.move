module lease_closeout::closeout {
    use std::vector;
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::event;

    public struct CloseoutRecord has store, copy, drop {
        unit_id: u64,
        assessed_damages: u64,
        deposit_amount: u64,
        landlord_payout: u64,
        tenant_payout: u64,
    }

    public struct CloseoutDesk has key {
        id: UID,
        records: vector<CloseoutRecord>,
    }

    public struct CloseoutProcessed has copy, drop {
        unit_id: u64,
        deposit_amount: u64,
        assessed_damages: u64,
        landlord_payout: u64,
        tenant_payout: u64,
    }

    fun init(ctx: &mut TxContext) {
        let desk = CloseoutDesk {
            id: object::new(ctx),
            records: vector[],
        };
        transfer::share_object(desk);
    }

    public fun process_closeout(
        desk: &mut CloseoutDesk,
        deposit: Coin<SUI>,
        assessed_damages: u64,
        unit_id: u64,
        landlord: address,
        tenant: address,
        ctx: &mut TxContext,
    ) {
        let deposit_amount = coin::value(&deposit);
        
        let (landlord_payout, tenant_payout) = if (assessed_damages >= deposit_amount) {
            (deposit_amount, 0)
        } else {
            (assessed_damages, deposit_amount - assessed_damages)
        };

        if (tenant_payout == 0) {
            transfer::public_transfer(deposit, landlord);
        } else {
            let landlord_coin = coin::split(&mut deposit, landlord_payout, ctx);
            transfer::public_transfer(landlord_coin, landlord);
            transfer::public_transfer(deposit, tenant);
        };

        let record = CloseoutRecord {
            unit_id,
            assessed_damages,
            deposit_amount,
            landlord_payout,
            tenant_payout,
        };

        vector::push_back(&mut desk.records, record);

        event::emit(CloseoutProcessed {
            unit_id,
            deposit_amount,
            assessed_damages,
            landlord_payout,
            tenant_payout,
        });
    }

    public fun get_closeouts(desk: &CloseoutDesk): &vector<CloseoutRecord> {
        &desk.records
    }
}
