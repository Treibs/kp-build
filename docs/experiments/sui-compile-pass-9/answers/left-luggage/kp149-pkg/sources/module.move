module luggage::luggage_office {
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::event;
    use std::vector;

    public struct OFFICE has drop {}

    public struct Bag has store {
        label: vector<u8>,
        forwarding_address: address,
    }

    public struct ClerkCapability has key, store {
        id: UID,
    }

    public struct LuggageOffice has key {
        id: UID,
        bags: vector<Bag>,
        fund: Balance<SUI>,
        courier_fee: u64,
    }

    public struct Forwarded has copy, drop {
        label: vector<u8>,
        forwarding_address: address,
    }

    fun init(_witness: OFFICE, ctx: &mut TxContext) {
        let office = LuggageOffice {
            id: object::new(ctx),
            bags: vector[],
            fund: balance::zero(),
            courier_fee: 1_000_000,
        };

        let cap = ClerkCapability {
            id: object::new(ctx),
        };

        transfer::share_object(office);
        transfer::transfer(cap, ctx.sender());
    }

    public fun deposit(
        office: &mut LuggageOffice,
        label: vector<u8>,
        forwarding_address: address,
        _ctx: &mut TxContext,
    ) {
        let bag = Bag {
            label,
            forwarding_address,
        };
        vector::push_back(&mut office.bags, bag);
    }

    public fun top_up(office: &mut LuggageOffice, payment: Coin<SUI>) {
        coin::put(&mut office.fund, payment);
    }

    public fun forward(
        office: &mut LuggageOffice,
        _cap: &ClerkCapability,
        index: u64,
        courier_address: address,
        ctx: &mut TxContext,
    ) {
        assert!(
            balance::value(&office.fund) >= office.courier_fee,
            0,
        );

        let bag = vector::remove(&mut office.bags, index);

        let payment = coin::take(&mut office.fund, office.courier_fee, ctx);
        transfer::public_transfer(payment, courier_address);

        event::emit(Forwarded {
            label: bag.label,
            forwarding_address: bag.forwarding_address,
        });
    }

    public fun bags_held(office: &LuggageOffice): u64 {
        vector::length(&office.bags)
    }

    public fun can_forward(office: &LuggageOffice): bool {
        balance::value(&office.fund) >= office.courier_fee
    }
}
