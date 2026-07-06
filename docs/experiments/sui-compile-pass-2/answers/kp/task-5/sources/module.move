/// kiosk_trade — place a KioskItem into a Sui Kiosk, list it for a fixed
/// price, and purchase it while resolving the TransferPolicy hot potato.
///
/// Move 2024 edition, targeting Sui mainnet (sui 1.74.x).
module kiosk_trade::kiosk_trade {
    use sui::kiosk::{Self, Kiosk, KioskOwnerCap};
    use sui::transfer_policy::{Self, TransferPolicy};
    use sui::package;
    use sui::coin::Coin;
    use sui::sui::SUI;
    use sui::event;
    use std::string::String;

    // -------------------------------------------------------------------------
    // One-time witness (must match module name in ALL_CAPS)
    // -------------------------------------------------------------------------

    public struct KIOSK_TRADE has drop {}

    // -------------------------------------------------------------------------
    // Tradeable item type — key + store so it can live inside a Kiosk and be
    // moved by transfer::public_transfer from any module.
    // -------------------------------------------------------------------------

    public struct KioskItem has key, store {
        id: UID,
        name: String,
        description: String,
    }

    // -------------------------------------------------------------------------
    // Events (must carry copy + drop)
    // -------------------------------------------------------------------------

    public struct ItemMinted has copy, drop {
        item_id: ID,
        name: String,
        creator: address,
    }

    public struct ItemListed has copy, drop {
        item_id: ID,
        kiosk_id: ID,
        price: u64,
    }

    public struct ItemPurchased has copy, drop {
        item_id: ID,
        price: u64,
        buyer: address,
    }

    // -------------------------------------------------------------------------
    // Module initializer
    //
    // Creates an open (rule-free) TransferPolicy<KioskItem> so purchases can
    // be confirmed immediately, shares the policy, and sends the cap and the
    // publisher to the deployer.
    // -------------------------------------------------------------------------

    fun init(otw: KIOSK_TRADE, ctx: &mut TxContext) {
        let publisher = package::claim(otw, ctx);
        let (policy, policy_cap) = transfer_policy::new<KioskItem>(&publisher, ctx);
        // Share the policy — any purchaser's PTB can reference it.
        transfer::public_share_object(policy);
        // Send capability objects to the deployer.
        transfer::public_transfer(policy_cap, ctx.sender());
        transfer::public_transfer(publisher, ctx.sender());
    }

    // -------------------------------------------------------------------------
    // Mint a new KioskItem and return it to the caller.
    // The PTB receiving it can then pass it to place_and_list.
    // -------------------------------------------------------------------------

    public fun mint_item(
        name: String,
        description: String,
        ctx: &mut TxContext,
    ): KioskItem {
        let id = object::new(ctx);
        let item_id = object::uid_to_inner(&id);
        let creator = ctx.sender();
        // *&name borrows and copies (String has copy) so `name` remains
        // available to move into the struct below.
        let name_for_event = *&name;
        event::emit(ItemMinted { item_id, name: name_for_event, creator });
        KioskItem { id, name, description }
    }

    // -------------------------------------------------------------------------
    // Create a new shared Kiosk and deliver the KioskOwnerCap to the caller.
    // -------------------------------------------------------------------------

    public fun create_kiosk(ctx: &mut TxContext) {
        let (kiosk, cap) = kiosk::new(ctx);
        transfer::public_share_object(kiosk);
        transfer::public_transfer(cap, ctx.sender());
    }

    // -------------------------------------------------------------------------
    // Place `item` into `kiosk` and immediately list it for `price` MIST.
    //
    // Caller must own the KioskOwnerCap that matches `kiosk`.
    // -------------------------------------------------------------------------

    public fun place_and_list(
        kiosk: &mut Kiosk,
        cap: &KioskOwnerCap,
        item: KioskItem,
        price: u64,
    ) {
        // Capture IDs before moving `item` into the kiosk.
        let item_id = object::id(&item);
        // &mut Kiosk is implicitly reborrowable as &Kiosk for object::id.
        let kiosk_id = object::id(kiosk);
        kiosk::place_and_list(kiosk, cap, item, price);
        event::emit(ItemListed { item_id, kiosk_id, price });
    }

    // -------------------------------------------------------------------------
    // Purchase a listed KioskItem.
    //
    // Flow:
    //   1. Call kiosk::purchase — transfers payment into the kiosk and returns
    //      the item plus a TransferRequest<KioskItem> hot potato.
    //   2. Resolve the hot potato via transfer_policy::confirm_request.
    //      Because the shared policy carries no rules, confirmation succeeds
    //      immediately.
    //   3. Deliver the item to the transaction sender.
    //
    // `payment` must equal the listed price exactly; kiosk::purchase aborts
    // on an amount mismatch.
    // -------------------------------------------------------------------------

    public fun purchase(
        kiosk: &mut Kiosk,
        policy: &TransferPolicy<KioskItem>,
        item_id: ID,
        payment: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        // Read price and buyer before consuming arguments.
        let price = payment.value();
        let buyer = ctx.sender();

        // Step 1: acquire the item and the hot potato.
        let (item, request) = kiosk::purchase<KioskItem>(kiosk, item_id, payment);

        // Step 2: resolve the hot potato.
        // confirm_request returns (ID, u64, address); all three have `drop`
        // so they are silently discarded when the call returns.
        transfer_policy::confirm_request(policy, request);

        // Step 3: emit and deliver.
        event::emit(ItemPurchased { item_id, price, buyer });
        transfer::public_transfer(item, buyer);
    }
}
