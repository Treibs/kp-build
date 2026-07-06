module my_nft::nft {
    use std::string::{Self, String};
    use sui::display;
    use sui::package;

    // ── One-time witness ──────────────────────────────────────────────────────
    // Field-less, `drop`-only, named after the module in ALL CAPS.
    // Cannot be constructed manually; received only in `init`.
    public struct NFT has drop {}

    // ── NFT object ────────────────────────────────────────────────────────────
    // `key + store` so the NFT can be publicly transferred from any module.
    // `id: UID` must be the first field (Sui E02007).
    public struct Nft has key, store {
        id: UID,
        name: String,
        image_url: String,
    }

    // ── Module initializer ────────────────────────────────────────────────────
    // Runs exactly once at publish time.
    // 1. Claims Publisher from the one-time witness.
    // 2. Creates Display<Nft> with `name` and `image_url` template fields.
    // 3. Freezes the Display (immutable shared object on-chain).
    // 4. Transfers the Publisher to the deployer for future upgrades.
    fun init(otw: NFT, ctx: &mut TxContext) {
        let publisher = package::claim(otw, ctx);

        let mut disp = display::new<Nft>(&publisher, ctx);
        // Template values reference Nft fields by name via `{field}` syntax.
        disp.add(string::utf8(b"name"),      string::utf8(b"{name}"));
        disp.add(string::utf8(b"image_url"), string::utf8(b"{image_url}"));
        // Bump the version counter so the Sui indexer picks up the new fields.
        disp.update_version();

        // Display is frozen — readable by anyone, immutable after publish.
        transfer::public_freeze_object(disp);

        // Publisher is transferred to the deployer (needed to update Display later).
        transfer::public_transfer(publisher, ctx.sender());
    }

    // ── Mint ──────────────────────────────────────────────────────────────────
    // Creates a fresh Nft and sends it to `recipient`.
    // Accepts raw byte vectors so callers don't need to construct String off-chain.
    public fun mint(
        name: vector<u8>,
        image_url: vector<u8>,
        recipient: address,
        ctx: &mut TxContext,
    ) {
        let nft = Nft {
            id: object::new(ctx),
            name: string::utf8(name),
            image_url: string::utf8(image_url),
        };
        transfer::public_transfer(nft, recipient);
    }

    // ── Accessors (method syntax) ─────────────────────────────────────────────

    public fun name(self: &Nft): &String {
        &self.name
    }

    public fun image_url(self: &Nft): &String {
        &self.image_url
    }
}
