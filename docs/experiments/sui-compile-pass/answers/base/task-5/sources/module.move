module guestbook::guestbook {

    use sui::clock::{Self, Clock};
    use sui::event;

    // ── Storage ──────────────────────────────────────────────────────────────

    /// Shared object that owns the list of all entries.
    public struct Guestbook has key {
        id: UID,
        entry_count: u64,
    }

    /// A single immutable guestbook entry stored on-chain.
    public struct Entry has key, store {
        id: UID,
        /// Sequential entry number (1-based).
        index: u64,
        /// Author's address.
        author: address,
        /// UTF-8 message, max 280 bytes enforced at runtime.
        message: vector<u8>,
        /// Unix timestamp in milliseconds from the on-chain Clock.
        timestamp_ms: u64,
    }

    // ── Events ────────────────────────────────────────────────────────────────

    public struct EntryAdded has copy, drop {
        index: u64,
        author: address,
        message: vector<u8>,
        timestamp_ms: u64,
    }

    // ── Errors ────────────────────────────────────────────────────────────────

    const EMessageTooLong: u64 = 0;
    const EMessageEmpty:   u64 = 1;

    // ── Constants ─────────────────────────────────────────────────────────────

    const MAX_MESSAGE_BYTES: u64 = 280;

    // ── Initialiser ───────────────────────────────────────────────────────────

    /// Called once at publish time; creates the shared Guestbook.
    fun init(ctx: &mut TxContext) {
        let book = Guestbook {
            id: object::new(ctx),
            entry_count: 0,
        };
        transfer::share_object(book);
    }

    // ── Public entry functions ────────────────────────────────────────────────

    /// Sign a guestbook entry.
    ///
    /// * `book`    – the shared Guestbook (mutable so we can bump the counter).
    /// * `clock`   – the shared `sui::clock::Clock` (address `0x6`).
    /// * `message` – UTF-8 bytes, 1–280 bytes.
    ///
    /// The resulting `Entry` is transferred to the caller.
    public entry fun sign(
        book: &mut Guestbook,
        clock: &Clock,
        message: vector<u8>,
        ctx: &mut TxContext,
    ) {
        let len = vector::length(&message);
        assert!(len > 0,               EMessageEmpty);
        assert!(len <= MAX_MESSAGE_BYTES, EMessageTooLong);

        book.entry_count = book.entry_count + 1;
        let index        = book.entry_count;
        let author       = tx_context::sender(ctx);
        let timestamp_ms = clock::timestamp_ms(clock);

        event::emit(EntryAdded {
            index,
            author,
            message: message,
            timestamp_ms,
        });

        let entry = Entry {
            id: object::new(ctx),
            index,
            author,
            message,
            timestamp_ms,
        };

        transfer::transfer(entry, author);
    }

    // ── Read-only helpers (callable off-chain or from other modules) ──────────

    public fun index(e: &Entry): u64          { e.index }
    public fun author(e: &Entry): address      { e.author }
    public fun message(e: &Entry): vector<u8>  { e.message }
    public fun timestamp_ms(e: &Entry): u64    { e.timestamp_ms }
    public fun entry_count(book: &Guestbook): u64 { book.entry_count }

    // ── Tests ─────────────────────────────────────────────────────────────────

    #[test_only]
    use sui::test_scenario::{Self as ts};
    #[test_only]
    use sui::clock as sui_clock;

    #[test]
    fun test_sign_creates_entry() {
        let alice = @0xA11CE;

        let mut scenario = ts::begin(alice);

        // Publish — runs init
        {
            init(ts::ctx(&mut scenario));
        };

        // Alice signs the book
        ts::next_tx(&mut scenario, alice);
        {
            let mut book  = ts::take_shared<Guestbook>(&scenario);
            let clock     = sui_clock::create_for_testing(ts::ctx(&mut scenario));

            let msg = b"Hello, Sui!";
            sign(&mut book, &clock, msg, ts::ctx(&mut scenario));

            assert!(entry_count(&book) == 1, 0);

            sui_clock::destroy_for_testing(clock);
            ts::return_shared(book);
        };

        // Verify Alice received an Entry
        ts::next_tx(&mut scenario, alice);
        {
            let entry = ts::take_from_sender<Entry>(&scenario);
            assert!(index(&entry)  == 1,           1);
            assert!(author(&entry) == alice,        2);
            assert!(message(&entry) == b"Hello, Sui!", 3);
            ts::return_to_sender(&scenario, entry);
        };

        ts::end(scenario);
    }

    #[test]
    #[expected_failure(abort_code = EMessageEmpty)]
    fun test_empty_message_aborts() {
        let alice = @0xA11CE;
        let mut scenario = ts::begin(alice);
        { init(ts::ctx(&mut scenario)); };

        ts::next_tx(&mut scenario, alice);
        {
            let mut book = ts::take_shared<Guestbook>(&scenario);
            let clock    = sui_clock::create_for_testing(ts::ctx(&mut scenario));
            sign(&mut book, &clock, b"", ts::ctx(&mut scenario));
            sui_clock::destroy_for_testing(clock);
            ts::return_shared(book);
        };
        ts::end(scenario);
    }

    #[test]
    #[expected_failure(abort_code = EMessageTooLong)]
    fun test_long_message_aborts() {
        let alice = @0xA11CE;
        let mut scenario = ts::begin(alice);
        { init(ts::ctx(&mut scenario)); };

        ts::next_tx(&mut scenario, alice);
        {
            let mut book = ts::take_shared<Guestbook>(&scenario);
            let clock    = sui_clock::create_for_testing(ts::ctx(&mut scenario));

            // Build a 281-byte message
            let mut msg = vector::empty<u8>();
            let mut i = 0u64;
            while (i < 281) {
                vector::push_back(&mut msg, 0x41u8); // 'A'
                i = i + 1;
            };

            sign(&mut book, &clock, msg, ts::ctx(&mut scenario));
            sui_clock::destroy_for_testing(clock);
            ts::return_shared(book);
        };
        ts::end(scenario);
    }
}
