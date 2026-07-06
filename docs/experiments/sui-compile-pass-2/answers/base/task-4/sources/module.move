module nft_collection::my_nft {
    use sui::display;
    use sui::object::{Self, UID};
    use sui::package;
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use std::string::{Self, String};

    // -----------------------------------------------------------------------
    // One-Time Witness
    // Must be named after the module in SCREAMING_SNAKE_CASE and carry only
    // the `drop` ability.  Sui guarantees exactly one instance ever exists,
    // which is what lets us safely claim the Publisher.
    // -----------------------------------------------------------------------
    public struct MY_NFT has drop {}

    // -----------------------------------------------------------------------
    // NFT object
    // `key` makes it a Sui object (gets a global UID).
    // `store` allows public transfer and wrapping by other objects.
    // Actual display metadata is resolved off-chain via the Display object.
    // -----------------------------------------------------------------------
    public struct Nft has key, store {
        id: UID,
        name: String,
        image_url: String,
    }

    // -----------------------------------------------------------------------
    // Module initialiser
    // Runs exactly once at publish time.
    // 1. Claims a Publisher from the one-time witness.
    // 2. Creates a Display<Nft> with `name` and `image_url` template fields.
    // 3. Calls update_version so the Sui indexer picks up the display object.
    // 4. Sends both Publisher and Display to the deployer.
    // -----------------------------------------------------------------------
    fun init(otw: MY_NFT, ctx: &mut TxContext) {
        let publisher = package::claim(otw, ctx);

        let keys = vector[
            string::utf8(b"name"),
            string::utf8(b"image_url"),
        ];
        let values = vector[
            // Template placeholders: {field_name} is replaced at query time
            // by the value stored in the on-chain Nft object.
            string::utf8(b"{name}"),
            string::utf8(b"{image_url}"),
        ];

        let mut disp = display::new_with_fields<Nft>(&publisher, keys, values, ctx);
        // Increment the version counter and emit a DisplayVersionUpdated event
        // so the off-chain indexer knows to re-resolve the template.
        display::update_version(&mut disp);

        let deployer = tx_context::sender(ctx);
        transfer::public_transfer(publisher, deployer);
        transfer::public_transfer(disp, deployer);
    }

    // -----------------------------------------------------------------------
    // Mint
    // Entry function: accepts raw UTF-8 bytes so it is callable directly from
    // the Sui CLI / SDK without a Move wrapper.
    // Creates a fresh Nft and sends it to the transaction sender.
    // -----------------------------------------------------------------------
    public entry fun mint(
        name: vector<u8>,
        image_url: vector<u8>,
        ctx: &mut TxContext,
    ) {
        let nft = Nft {
            id: object::new(ctx),
            name: string::utf8(name),
            image_url: string::utf8(image_url),
        };
        transfer::public_transfer(nft, tx_context::sender(ctx));
    }
}
