/// A minimal Sui Kiosk marketplace module.
///
/// Two entry points:
///   • place_and_list — kiosk owner deposits an item and lists it at a fixed price.
///   • purchase       — buyer pays, the TransferRequest hot potato is confirmed
///                      against the item's TransferPolicy, and the item is
///                      delivered to the buyer.
///
/// Move 2024 edition · Sui mainnet toolchain
module kiosk_trade::marketplace {

    use sui::kiosk::{Self, Kiosk, KioskOwnerCap};
    use sui::transfer_policy::{Self, TransferPolicy, TransferRequest};
    use sui::coin::Coin;
    use sui::sui::SUI;
    use sui::object::ID;
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};

    // ─── Error codes ───────────────────────────────────────────────────────────

    /// The listing price must be at least 1 MIST.
    const EZeroPrice: u64 = 0;

    // ─── Owner-side ────────────────────────────────────────────────────────────

    /// Deposit `item` into `kiosk` and immediately list it for sale at `price`
    /// MIST.
    ///
    /// Arguments
    /// ---------
    /// kiosk  — the seller's Kiosk object (must be owned by `cap`).
    /// cap    — KioskOwnerCap proving the caller controls `kiosk`.
    /// item   — the asset to sell; must have `key + store`.
    /// price  — fixed listing price in MIST; aborts with EZeroPrice if zero.
    ///
    /// The kiosk framework tracks the item internally; no further action is
    /// required from the seller until a buyer calls `purchase`.
    public fun place_and_list<T: key + store>(
        kiosk:  &mut Kiosk,
        cap:    &KioskOwnerCap,
        item:   T,
        price:  u64,
        _ctx:   &mut TxContext,
    ) {
        assert!(price > 0, EZeroPrice);
        // Atomically places the item into the kiosk's locked inventory and
        // creates a public listing at the given price.
        kiosk::place_and_list(kiosk, cap, item, price);
    }

    // ─── Buyer-side ────────────────────────────────────────────────────────────

    /// Purchase the item identified by `id` from `kiosk`, paying with `payment`.
    ///
    /// Internal sequence
    /// -----------------
    ///   1. `kiosk::purchase` debits the exact listing price from `payment`
    ///      (returning any overpayment to the kiosk profits), removes the item
    ///      from the listing, and produces a `TransferRequest<T>` hot potato
    ///      that MUST be destroyed before the transaction ends.
    ///
    ///   2. `transfer_policy::confirm_request` destroys the hot potato after
    ///      verifying that every rule registered on `policy` has emitted its
    ///      receipt.  A policy with no rules is satisfied trivially.  Aborts
    ///      with `EPolicyNotSatisfied` if any rule is outstanding.
    ///
    ///   3. The item is transferred to the transaction sender.
    ///
    /// Rules with intermediate steps (royalties, allowlists, …)
    /// ---------------------------------------------------------
    /// If the `TransferPolicy` has rules that require intermediate on-chain
    /// actions (e.g. paying a royalty into a separate object), those steps must
    /// be fulfilled — and the resulting receipt added to the request — before
    /// `confirm_request` is called.  In that scenario compose the lower-level
    /// primitives (`kiosk::purchase` → rule-fulfillment calls →
    /// `transfer_policy::confirm_request`) inside a single programmable
    /// transaction block instead of calling this wrapper.
    public fun purchase<T: key + store>(
        kiosk:   &mut Kiosk,
        id:      ID,
        payment: Coin<SUI>,
        policy:  &TransferPolicy<T>,
        ctx:     &mut TxContext,
    ) {
        // ── Step 1: buy the item and receive the hot potato ──────────────────
        //
        // kiosk::purchase signature:
        //   public fun purchase<T: key + store>(
        //       self: &mut Kiosk, id: ID, payment: Coin<SUI>
        //   ): (T, TransferRequest<T>)
        let (item, request): (T, TransferRequest<T>) =
            kiosk::purchase(kiosk, id, payment);

        // ── Step 2: resolve the TransferRequest hot potato ───────────────────
        //
        // transfer_policy::confirm_request signature:
        //   public fun confirm_request<T>(
        //       self: &TransferPolicy<T>, request: TransferRequest<T>
        //   ): (u64, ID, ID)            // (amount_paid, from_kiosk_id, item_id)
        //
        // The hot potato has no `drop` ability, so it cannot be silently
        // discarded — confirm_request is the only way to destroy it.
        let (_amount_paid, _from_kiosk, _item_id) =
            transfer_policy::confirm_request(policy, request);

        // ── Step 3: deliver the item to the buyer ────────────────────────────
        //
        // public_transfer is appropriate because T: key + store means the type
        // has declared its intent to be transferable across module boundaries.
        transfer::public_transfer(item, tx_context::sender(ctx));
    }
}
