module lease_closeout::desk {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::event;
    use sui::table::{Self, Table};

    public struct InspectorCap has key, store {
        id: UID,
    }

    public struct Desk has key {
        id: UID,
        closeouts: Table<u64, CloseoutRecord>,
        count: u64,
    }

    public struct CloseoutRecord has store {
        landlord: address,
        tenant: address,
        deposit_amount: u64,
        assessed_damages: u64,
        landlord_payout: u64,
        tenant_refund: u64,
    }

    public struct CloseoutProcessed has copy, drop {
        landlord: address,
        tenant: address,
        deposit: u64,
        damages: u64,
        landlord_payout: u64,
        tenant_refund: u64,
    }

    fun init(ctx: &mut TxContext) {
        let inspector_cap = InspectorCap {
            id: object::new(ctx),
        };
        transfer::transfer(inspector_cap, ctx.sender());

        let desk = Desk {
            id: object::new(ctx),
            closeouts: table::new(ctx),
            count: 0,
        };
        transfer::share_object(desk);
    }

    public fun process_closeout(
        deposit: Coin<SUI>,
        assessed_damages: u64,
        landlord: address,
        tenant: address,
        _cap: &InspectorCap,
        desk: &mut Desk,
        ctx: &mut TxContext,
    ) {
        let deposit_amount = coin::value(&deposit);
        
        let landlord_payout = if (assessed_damages >= deposit_amount) {
            deposit_amount
        } else {
            assessed_damages
        };
        
        let tenant_refund = deposit_amount - landlord_payout;

        let mut remaining = deposit;
        let landlord_coin = coin::split(&mut remaining, landlord_payout, ctx);

        let closeout = CloseoutRecord {
            landlord,
            tenant,
            deposit_amount,
            assessed_damages,
            landlord_payout,
            tenant_refund,
        };

        table::add(&mut desk.closeouts, desk.count, closeout);
        desk.count = desk.count + 1;

        event::emit(CloseoutProcessed {
            landlord,
            tenant,
            deposit: deposit_amount,
            damages: assessed_damages,
            landlord_payout,
            tenant_refund,
        });

        transfer::public_transfer(landlord_coin, landlord);
        transfer::public_transfer(remaining, tenant);
    }

    public fun get_closeout(desk: &Desk, index: u64): &CloseoutRecord {
        table::borrow(&desk.closeouts, index)
    }

    public fun closeout_count(desk: &Desk): u64 {
        desk.count
    }
}
