/// Atomic two-party object swap.
///
/// Flow
/// ----
/// 1. Party A calls `create`, depositing object `T` into a shared escrow and
///    naming party B as the recipient.
/// 2. Party B calls `swap`, providing object `U`. The escrow atomically
///    delivers `T` to party B and `U` to party A in a single transaction.
/// 3. Before party B acts, party A may call `cancel` to reclaim `T`.
module escrow::atomic_swap {

    use sui::event;
    use sui::object::ID;

    // ── Error codes ───────────────────────────────────────────────────────────

    const ENotRecipient: u64 = 0;
    const ENotSender:    u64 = 1;

    // ── Storage ───────────────────────────────────────────────────────────────

    /// Shared escrow holding one item of type `T` until a swap is completed or
    /// the sender cancels.  `T` must have `key + store` so it can be held
    /// inside another object and transferred unconditionally.
    public struct Escrow<T: key + store> has key {
        id: UID,
        /// Address that created the escrow and deposited `item` (party A).
        sender: address,
        /// Address that must supply the counter-offer to complete the swap (party B).
        recipient: address,
        /// The escrowed object awaiting the swap.
        item: T,
    }

    // ── Events ────────────────────────────────────────────────────────────────

    public struct EscrowCreated has copy, drop {
        escrow_id: ID,
        sender:    address,
        recipient: address,
    }

    public struct SwapCompleted has copy, drop {
        escrow_id: ID,
        sender:    address,
        recipient: address,
    }

    public struct EscrowCancelled has copy, drop {
        escrow_id: ID,
        sender:    address,
    }

    // ── Public API ────────────────────────────────────────────────────────────

    /// Party A creates the escrow, locking `item` inside and naming the
    /// `recipient` who may complete the swap.  The `Escrow` is immediately
    /// shared so both parties can interact with it without either holding it
    /// in their wallet.
    public fun create<T: key + store>(
        item: T,
        recipient: address,
        ctx: &mut TxContext,
    ) {
        let sender = ctx.sender();
        let escrow = Escrow {
            id: object::new(ctx),
            sender,
            recipient,
            item,
        };
        event::emit(EscrowCreated {
            escrow_id: object::id(&escrow),
            sender,
            recipient,
        });
        transfer::share_object(escrow);
    }

    /// Party B completes the swap by supplying `incoming` (type `U`).
    ///
    /// Atomically:
    ///   - party B (the caller) receives the escrowed `T`
    ///   - party A (the original sender) receives `U`
    ///
    /// Aborts with `ENotRecipient` if the caller is not the named recipient.
    public fun swap<T: key + store, U: key + store>(
        escrow: Escrow<T>,
        incoming: U,
        ctx: &mut TxContext,
    ) {
        assert!(ctx.sender() == escrow.recipient, ENotRecipient);
        let Escrow { id, sender, recipient, item } = escrow;
        event::emit(SwapCompleted {
            escrow_id: object::uid_to_inner(&id),
            sender,
            recipient,
        });
        object::delete(id);
        // Deliver the escrowed item to party B (the recipient / caller).
        transfer::public_transfer(item, recipient);
        // Deliver the counter-offer to party A (the original sender).
        transfer::public_transfer(incoming, sender);
    }

    /// Party A cancels the escrow and reclaims the deposited object.
    ///
    /// Aborts with `ENotSender` if the caller is not the original creator.
    public fun cancel<T: key + store>(
        escrow: Escrow<T>,
        ctx: &mut TxContext,
    ) {
        assert!(ctx.sender() == escrow.sender, ENotSender);
        let Escrow { id, sender, recipient: _recipient, item } = escrow;
        event::emit(EscrowCancelled {
            escrow_id: object::uid_to_inner(&id),
            sender,
        });
        object::delete(id);
        transfer::public_transfer(item, sender);
    }
}
