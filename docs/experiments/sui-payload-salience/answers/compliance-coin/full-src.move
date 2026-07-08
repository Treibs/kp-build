module regulated::regulated_token {
    use sui::coin::{Self, Coin, TreasuryCap};
    use sui::table;

    public struct REGULATED_TOKEN has drop {}

    public struct ComplianceCap has key, store {
        id: UID,
    }

    public struct FrozenRegistry has key {
        id: UID,
        frozen: table::Table<address, bool>,
    }

    fun init(witness: REGULATED_TOKEN, ctx: &mut TxContext) {
        let (treasury, metadata) = coin::create_currency(
            witness,
            9,
            b"REG",
            b"Regulated Token",
            b"A regulated token with compliance controls",
            option::none(),
            ctx,
        );

        let compliance_cap = ComplianceCap {
            id: object::new(ctx),
        };

        let frozen_registry = FrozenRegistry {
            id: object::new(ctx),
            frozen: table::new(ctx),
        };

        transfer::transfer(treasury, ctx.sender());
        transfer::transfer(compliance_cap, ctx.sender());
        transfer::share_object(frozen_registry);

        transfer::public_freeze_object(metadata);
    }

    public fun freeze_address(
        _cap: &ComplianceCap,
        registry: &mut FrozenRegistry,
        addr: address,
    ) {
        if (!table::contains(&registry.frozen, addr)) {
            table::add(&mut registry.frozen, addr, true);
        };
    }

    public fun unfreeze_address(
        _cap: &ComplianceCap,
        registry: &mut FrozenRegistry,
        addr: address,
    ) {
        if (table::contains(&registry.frozen, addr)) {
            table::remove(&mut registry.frozen, addr);
        };
    }

    public fun is_frozen(registry: &FrozenRegistry, addr: address): bool {
        table::contains(&registry.frozen, addr)
    }

    public fun mint(
        treasury_cap: &mut TreasuryCap<REGULATED_TOKEN>,
        amount: u64,
        recipient: address,
        registry: &FrozenRegistry,
        ctx: &mut TxContext,
    ) {
        assert!(!is_frozen(registry, recipient), 0);
        let coin = coin::mint(treasury_cap, amount, ctx);
        transfer::public_transfer(coin, recipient);
    }

    public fun transfer_coins(
        coin: Coin<REGULATED_TOKEN>,
        recipient: address,
        registry: &FrozenRegistry,
        ctx: &TxContext,
    ) {
        let sender = ctx.sender();
        assert!(!is_frozen(registry, sender), 1);
        assert!(!is_frozen(registry, recipient), 2);
        transfer::public_transfer(coin, recipient);
    }
}
