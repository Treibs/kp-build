module kits::kits {

    use sui::coin::{Self, Coin, TreasuryCap};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};

    /// The one-time witness type for the KITS coin.
    public struct KITS has drop {}

    /// Capability held by the contract admin that enforces the supply cap.
    public struct MintCap has key, store {
        id: UID,
        treasury_cap: TreasuryCap<KITS>,
        max_supply: u64,
        minted: u64,
    }

    /// Total hard cap: 1,000,000,000 KITS (9 decimals → 10^9 base units per KITS).
    const MAX_SUPPLY: u64 = 1_000_000_000_000_000_000; // 10^18 base units total

    /// Error codes.
    const EExceedsCap: u64 = 0;

    /// Called once on publish.  Creates the coin metadata and hands the
    /// wrapped MintCap to the deployer.
    fun init(witness: KITS, ctx: &mut TxContext) {
        let (treasury_cap, metadata) = coin::create_currency(
            witness,
            9,                          // decimals
            b"KITS",                    // symbol
            b"Acorn Token",           // name
            b"Capped fungible token for the Acorn ecosystem.",
            option::none(),             // icon_url
            ctx,
        );

        // Freeze the metadata so nobody can change name/symbol later.
        transfer::public_freeze_object(metadata);

        // Wrap TreasuryCap inside MintCap so raw minting is impossible
        // without going through our cap-check logic.
        let mint_cap = MintCap {
            id: object::new(ctx),
            treasury_cap,
            max_supply: MAX_SUPPLY,
            minted: 0,
        };

        transfer::transfer(mint_cap, tx_context::sender(ctx));
    }

    /// Mint `amount` KITS to `recipient`.  Aborts if the total minted would
    /// exceed `MAX_SUPPLY`.
    public fun mint(
        cap: &mut MintCap,
        amount: u64,
        recipient: address,
        ctx: &mut TxContext,
    ) {
        assert!(cap.minted + amount <= cap.max_supply, EExceedsCap);
        cap.minted = cap.minted + amount;
        let coin = coin::mint(&mut cap.treasury_cap, amount, ctx);
        transfer::public_transfer(coin, recipient);
    }

    /// Burn `coin`, reducing the circulating supply.
    /// The cap ceiling is NOT relaxed on burn (burn is permanent destruction,
    /// not a recycling mechanism).  Remove this constraint and decrement
    /// `cap.minted` if you want a rebasing/recycling design instead.
    public fun burn(cap: &mut MintCap, coin: Coin<KITS>) {
        coin::burn(&mut cap.treasury_cap, coin);
    }

    /// Read-only helpers.
    public fun max_supply(cap: &MintCap): u64 { cap.max_supply }
    public fun minted(cap: &MintCap): u64 { cap.minted }
    public fun remaining(cap: &MintCap): u64 { cap.max_supply - cap.minted }
}
