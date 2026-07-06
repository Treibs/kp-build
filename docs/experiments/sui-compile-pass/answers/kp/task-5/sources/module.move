/// A shared on-chain guestbook where anyone can leave a timestamped message.
/// The timestamp is sourced from the Sui network Clock object (address 0x6)
/// and cannot be forged by the transaction sender.
module guestbook::guestbook {

    use std::string::String;
    use sui::clock::Clock;
    use sui::event;

    // ─── Storage types ────────────────────────────────────────────────────────

    /// One guestbook entry stored inside the shared Guestbook vector.
    public struct Entry has store {
        /// Address of the account that signed this entry.
        author: address,
        /// Free-form message left by the signer.
        message: String,
        /// Unix-epoch time in milliseconds at the moment of signing,
        /// sourced from the on-chain Clock — not chosen by the sender.
        timestamp_ms: u64,
    }

    /// The shared guestbook object that holds all entries.
    /// Created once in `init` and shared with the network.
    public struct Guestbook has key {
        id: UID,
        entries: vector<Entry>,
    }

    // ─── Events ───────────────────────────────────────────────────────────────

    /// Emitted whenever a new entry is added.
    /// address, String, and u64 all carry `copy + drop`, satisfying
    /// the event::emit<T: copy + drop> constraint.
    public struct EntrySigned has copy, drop {
        author: address,
        message: String,
        timestamp_ms: u64,
        /// Zero-based index of the new entry inside Guestbook.entries.
        entry_index: u64,
    }

    // ─── Module initializer ───────────────────────────────────────────────────

    fun init(ctx: &mut TxContext) {
        transfer::share_object(Guestbook {
            id: object::new(ctx),
            entries: vector::empty(),
        });
    }

    // ─── Public functions ─────────────────────────────────────────────────────

    /// Sign the guestbook with `message`.
    ///
    /// Callers must supply the shared Clock object (address 0x6).
    /// `clock.timestamp_ms()` is evaluated on-chain at checkpoint time;
    /// the stored timestamp reflects the network clock, not a value
    /// the caller could supply or manipulate.
    ///
    /// address, String, and u64 all have the `copy` ability, so the compiler
    /// inserts implicit copies allowing each binding to appear in both the
    /// stored Entry and the emitted event without a double-move error.
    public fun sign(
        guestbook: &mut Guestbook,
        clock: &Clock,
        message: String,
        ctx: &mut TxContext,
    ) {
        let author = ctx.sender();
        let timestamp_ms = clock.timestamp_ms();
        let entry_index = guestbook.entries.length();
        guestbook.entries.push_back(Entry { author, message, timestamp_ms });
        event::emit(EntrySigned { author, message, timestamp_ms, entry_index });
    }

    /// Total number of entries currently in the guestbook.
    public fun entry_count(guestbook: &Guestbook): u64 {
        guestbook.entries.length()
    }

    /// Signer address of the entry at `index`.
    public fun entry_author(guestbook: &Guestbook, index: u64): address {
        vector::borrow(&guestbook.entries, index).author
    }

    /// On-chain timestamp (Unix milliseconds) of the entry at `index`.
    public fun entry_timestamp_ms(guestbook: &Guestbook, index: u64): u64 {
        vector::borrow(&guestbook.entries, index).timestamp_ms
    }

    /// Message text of the entry at `index`.
    /// Returns a copy (String has `copy`).
    public fun entry_message(guestbook: &Guestbook, index: u64): String {
        vector::borrow(&guestbook.entries, index).message
    }
}
