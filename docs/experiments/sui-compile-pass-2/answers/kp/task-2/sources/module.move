/// Object mailbox — a shared on-chain inbox controlled by a capability.
///
/// Anyone may send an object of type `T` (defined inside this package) to the
/// `Mailbox` by calling `transfer::transfer(item, mailbox_address)` from their
/// own module.  Only the holder of the matching `OwnerCap` can call `open` to
/// withdraw those objects.
///
/// Note on `transfer::receive`
/// ───────────────────────────
/// Sui's bytecode verifier permits `transfer::receive<T: key>` only when the
/// call site is inside the package that defines `T`.  This mailbox therefore
/// works for any `T` defined within this same package.  To receive objects
/// whose type is defined in a foreign package and carries the `store` ability,
/// replace `transfer::receive` with `transfer::public_receive` and widen the
/// bound to `T: key + store`.
module mailbox::mailbox {
    use sui::transfer::Receiving;
    use sui::object::ID;
    use sui::event;

    // ─── Object types ─────────────────────────────────────────────────────

    /// On-chain mailbox.  Shared so that any party may address objects to it.
    public struct Mailbox has key {
        id: UID,
    }

    /// Proof of ownership over a specific `Mailbox`.
    ///
    /// A function gated on `&OwnerCap` can only be invoked by whoever currently
    /// holds this object — possession of the cap IS the authorisation.
    public struct OwnerCap has key, store {
        id: UID,
        /// The on-chain ID of the `Mailbox` this cap is bound to.
        mailbox_id: ID,
    }

    // ─── Events ───────────────────────────────────────────────────────────

    /// Emitted whenever a new `Mailbox` is created.
    public struct MailboxCreated has copy, drop {
        mailbox_id: ID,
    }

    // ─── Constructor ──────────────────────────────────────────────────────

    /// Create a new shared `Mailbox` and return the `OwnerCap` that controls it.
    ///
    /// The caller is responsible for transferring (or otherwise consuming) the
    /// returned cap, e.g. via `transfer::public_transfer(cap, ctx.sender())`.
    public fun create(ctx: &mut TxContext): OwnerCap {
        let mailbox = Mailbox { id: object::new(ctx) };
        let mailbox_id = object::id(&mailbox);
        event::emit(MailboxCreated { mailbox_id });
        transfer::share_object(mailbox);
        OwnerCap {
            id: object::new(ctx),
            mailbox_id,
        }
    }

    // ─── Core receive ─────────────────────────────────────────────────────

    /// Extract an object previously sent to `mailbox`.
    ///
    /// * `cap`    – must be the `OwnerCap` bound to this specific `Mailbox`;
    ///              aborts if the IDs do not match.
    /// * `ticket` – the `Receiving<T>` ticket representing the pending object.
    ///
    /// Returns the extracted `T`; the caller must transfer or otherwise consume
    /// it (e.g. forward it onward with `transfer::public_transfer`).
    public fun open<T: key>(
        mailbox: &mut Mailbox,
        cap: &OwnerCap,
        ticket: Receiving<T>,
    ): T {
        assert!(cap.mailbox_id == object::id(mailbox));
        transfer::receive(&mut mailbox.id, ticket)
    }

    // ─── Accessors ────────────────────────────────────────────────────────

    /// Return the on-chain ID of `mailbox`.
    public fun mailbox_id(mailbox: &Mailbox): ID {
        object::id(mailbox)
    }

    /// Return the mailbox ID stored inside `cap`.
    public fun cap_mailbox_id(cap: &OwnerCap): ID {
        cap.mailbox_id
    }
}
