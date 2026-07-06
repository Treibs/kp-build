module kits::kits {
    use sui::coin::{Self, TreasuryCap, CoinMetadata};
    use sui::event;

    // ─── One-time witness ────────────────────────────────────────────────────
    // Field-less, drop-only, named after the module in ALL_CAPS — required by
    // coin::create_currency and the init signature checker.
    public struct KITS has drop {}

    // ─── Mint capability ─────────────────────────────────────────────────────
    // Wraps TreasuryCap so that every mint path goes through the cap check.
    // key + store → freely transferable with transfer::public_transfer.
    public struct KitsMintCap has key, store {
        id: UID,
        treasury: TreasuryCap<KITS>,
        max_supply: u64,
    }

    // ─── Events ──────────────────────────────────────────────────────────────
    // emit<T> requires T: copy + drop — both abilities are declared here.
    public struct TokensMinted has copy, drop {
        amount: u64,
        recipient: address,
        new_total_supply: u64,
    }

    public struct TokensBurned has copy, drop {
        amount: u64,
        new_total_supply: u64,
    }

    // ─── Error codes ─────────────────────────────────────────────────────────
    const ESupplyCapExceeded: u64 = 0;

    // ─── Module initializer ──────────────────────────────────────────────────
    // First parameter must be the one-time witness; init runs exactly once
    // at publish time.  coin::create_currency consumes the OTW.
    fun init(witness: KITS, ctx: &mut TxContext) {
        let (treasury, metadata) = coin::create_currency(
            witness,
            9,                      // decimals
            b"KITS",                // symbol
            b"Acorn",             // name
            b"KITS fungible token with a hard-capped total supply",
            option::none(),         // icon URL — Option<sui::url::Url>
            ctx,
        );

        // Hard cap: 1 000 000 000 KITS at 9-decimal precision.
        let mint_cap = KitsMintCap {
            id: object::new(ctx),
            treasury,
            max_supply: 1_000_000_000__000_000_000,
        };

        // Freeze metadata so coin details are immutable on-chain.
        transfer::public_freeze_object(metadata);

        // Deliver the mint cap to the deployer.
        transfer::public_transfer(mint_cap, ctx.sender());
    }

    // ─── Mint ─────────────────────────────────────────────────────────────────
    // Enforces the cap before minting.  Any overshoot aborts the transaction.
    public fun mint(
        cap: &mut KitsMintCap,
        amount: u64,
        recipient: address,
        ctx: &mut TxContext,
    ) {
        let current = coin::total_supply(&cap.treasury);
        // Move arithmetic aborts on overflow, so the add is inherently safe.
        assert!(current + amount <= cap.max_supply, ESupplyCapExceeded);

        let minted = coin::mint(&mut cap.treasury, amount, ctx);

        event::emit(TokensMinted {
            amount,
            recipient,
            new_total_supply: current + amount,
        });

        transfer::public_transfer(minted, recipient);
    }

    // ─── Burn ─────────────────────────────────────────────────────────────────
    // Destroys tokens and reduces total supply, freeing headroom under the cap.
    public fun burn(
        cap: &mut KitsMintCap,
        token: coin::Coin<KITS>,
    ) {
        let amount = coin::value(&token);
        coin::burn(&mut cap.treasury, token);

        event::emit(TokensBurned {
            amount,
            new_total_supply: coin::total_supply(&cap.treasury),
        });
    }

    // ─── Read-only accessors ──────────────────────────────────────────────────
    public fun max_supply(cap: &KitsMintCap): u64 {
        cap.max_supply
    }

    public fun total_supply(cap: &KitsMintCap): u64 {
        coin::total_supply(&cap.treasury)
    }

    public fun remaining_supply(cap: &KitsMintCap): u64 {
        cap.max_supply - coin::total_supply(&cap.treasury)
    }
}
