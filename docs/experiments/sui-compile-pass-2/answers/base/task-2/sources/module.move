/// mailbox — a shared on-chain "inbox" that accepts any key object sent to its
/// address; only the holder of the matching MailboxOwnerCap may withdraw items.
module mailbox::mailbox {
    use sui::transfer::{Self, Receiving};
    use sui::object::{Self, UID, ID};
    use sui::tx_context::{Self, TxContext};

    // ── Error codes ──────────────────────────────────────────────────────────

    /// The capability does not match the supplied mailbox.
    const ECapMailboxMismatch: u64 = 0;

    // ── Object types ─────────────────────────────────────────────────────────

    /// Shared on-chain mailbox.  Any account or contract may send a `key`
    /// object to `object::id_address(&mailbox)` using `transfer::public_transfer`.
    public struct Mailbox has key {
        id: UID,
    }

    /// Proof of ownership for a specific `Mailbox`.
    /// The holder is entitled to call `open` and extract objects from it.
    /// Intentionally not `drop` — losing the cap means losing mailbox access.
    public struct MailboxOwnerCap has key, store {
        id: UID,
        /// The ID of the `Mailbox` this capability controls.
        mailbox_id: ID,
    }

    // ── Construction ─────────────────────────────────────────────────────────

    /// Create a new `Mailbox` (shared) and deliver the `MailboxOwnerCap`
    /// to the transaction sender.
    public entry fun new(ctx: &mut TxContext) {
        let mailbox = Mailbox { id: object::new(ctx) };
        let mailbox_id = object::id(&mailbox);
        transfer::share_object(mailbox);

        transfer::transfer(
            MailboxOwnerCap { id: object::new(ctx), mailbox_id },
            tx_context::sender(ctx),
        );
    }

    // ── Core logic ───────────────────────────────────────────────────────────

    /// Extract an object of type `T` that was sent to this mailbox.
    ///
    /// Parameters
    /// - `cap`     : owner capability — must belong to `mailbox`
    /// - `mailbox` : the shared `Mailbox` shared object
    /// - `ticket`  : `Receiving<T>` ticket produced by the Sui runtime for
    ///               an object previously sent to the mailbox's address
    ///
    /// Aborts
    /// - `ECapMailboxMismatch` when `cap.mailbox_id` does not equal
    ///   `object::id(mailbox)`.
    public fun open<T: key>(
        cap: &MailboxOwnerCap,
        mailbox: &mut Mailbox,
        ticket: Receiving<T>,
    ): T {
        assert!(cap.mailbox_id == object::id(mailbox), ECapMailboxMismatch);
        transfer::receive(&mut mailbox.id, ticket)
    }

    // ── Read-only helpers ─────────────────────────────────────────────────────

    /// Return the ID of the mailbox a capability controls.
    public fun cap_mailbox_id(cap: &MailboxOwnerCap): ID {
        cap.mailbox_id
    }
}
