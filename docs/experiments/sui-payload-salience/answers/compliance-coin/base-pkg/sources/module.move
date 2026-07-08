module regulated_token::reg_token {
    use sui::coin::{Self, Coin, TreasuryCap};
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use std::option;
    use std::vector;

    public struct REG has drop {}

    public struct ComplianceCapability has key {
        id: UID,
        frozen_addresses: vector<address>,
    }

    fun init(otw: REG, ctx: &mut TxContext) {
        let (treasury_cap, metadata) = coin::create_currency(
            otw,
            9,
            b"REG",
            b"Regulated Token",
            b"A regulated token with compliance controls",
            option::none(),
            ctx,
        );

        let compliance_cap = ComplianceCapability {
            id: object::new(ctx),
            frozen_addresses: vector::empty(),
        };

        transfer::public_transfer(treasury_cap, tx_context::sender(ctx));
        transfer::transfer(compliance_cap, tx_context::sender(ctx));
        transfer::public_share_object(metadata);
    }

    public entry fun mint(
        treasury_cap: &mut TreasuryCap<REG>,
        amount: u64,
        recipient: address,
        compliance_cap: &ComplianceCapability,
        ctx: &mut TxContext,
    ) {
        assert!(!is_frozen(compliance_cap, recipient), 1);
        let coin = coin::mint(treasury_cap, amount, ctx);
        transfer::public_transfer(coin, recipient);
    }

    public entry fun transfer_with_guard(
        coin: Coin<REG>,
        recipient: address,
        compliance_cap: &ComplianceCapability,
        ctx: &TxContext,
    ) {
        let sender = tx_context::sender(ctx);
        assert!(!is_frozen(compliance_cap, sender), 2);
        assert!(!is_frozen(compliance_cap, recipient), 3);
        transfer::public_transfer(coin, recipient);
    }

    public fun is_frozen(compliance_cap: &ComplianceCapability, addr: address): bool {
        vector::contains(&compliance_cap.frozen_addresses, &addr)
    }

    public entry fun freeze_address(
        compliance_cap: &mut ComplianceCapability,
        addr: address,
    ) {
        if (!vector::contains(&compliance_cap.frozen_addresses, &addr)) {
            vector::push_back(&mut compliance_cap.frozen_addresses, addr);
        }
    }

    public entry fun unfreeze_address(
        compliance_cap: &mut ComplianceCapability,
        addr: address,
    ) {
        let (found, index) = vector::index_of(&compliance_cap.frozen_addresses, &addr);
        if (found) {
            vector::remove(&mut compliance_cap.frozen_addresses, index);
        }
    }
}
