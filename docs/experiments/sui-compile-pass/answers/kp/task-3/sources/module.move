module soulbound_badge::badge {
    use sui::event;
    use sui::clock::Clock;
    use sui::object::ID;

    // ─── Types ────────────────────────────────────────────────────────────────

    /// Soulbound badge. Declared `key`-only — no `store`.
    ///
    /// The missing `store` ability is the compile-time transfer lock:
    ///   • `transfer::public_transfer<T: key + store>` cannot be instantiated for
    ///     this type; any module outside this one that attempts it gets E05001.
    ///   • `transfer::transfer<T: key>` is valid but callable only from the
    ///     defining module; since we never re-export a transfer function, the
    ///     badge is permanently locked to its initial recipient after mint.
    public struct Badge has key {
        id: UID,
        /// Address the badge was originally issued to.
        recipient: address,
        /// Human-readable badge name (UTF-8 bytes).
        name: vector<u8>,
        /// Longer description (UTF-8 bytes).
        description: vector<u8>,
        /// Mint timestamp in milliseconds sourced from the on-chain Clock.
        issued_at_ms: u64,
    }

    /// Capability that authorises minting.
    /// Transferred to the deployer in `init`; `store` lets it be wrapped or
    /// re-transferred without a custom transfer function.
    public struct MinterCap has key, store {
        id: UID,
    }

    // ─── Events ───────────────────────────────────────────────────────────────

    /// Emitted when a new badge is minted and delivered.
    public struct BadgeIssued has copy, drop {
        badge_id: ID,
        recipient: address,
    }

    /// Emitted when a badge is voluntarily burned by its holder.
    public struct BadgeBurned has copy, drop {
        badge_id: ID,
        recipient: address,
    }

    // ─── Initialiser ──────────────────────────────────────────────────────────

    /// Runs once at publish time. Delivers the sole MinterCap to the deployer.
    fun init(ctx: &mut TxContext) {
        transfer::transfer(
            MinterCap { id: object::new(ctx) },
            ctx.sender(),
        );
    }

    // ─── Public API ───────────────────────────────────────────────────────────

    /// Mint a soulbound badge and deliver it directly to `recipient`.
    ///
    /// Gated on `MinterCap`: only the holder of that capability may issue badges.
    /// Time is read from the shared `Clock` object (address 0x6).
    public fun mint(
        _cap: &MinterCap,
        recipient: address,
        name: vector<u8>,
        description: vector<u8>,
        clock: &Clock,
        ctx: &mut TxContext,
    ) {
        let badge = Badge {
            id: object::new(ctx),
            recipient,
            name,
            description,
            issued_at_ms: clock.timestamp_ms(),
        };
        // Capture the ID before moving `badge` into transfer.
        let badge_id = object::id(&badge);
        event::emit(BadgeIssued { badge_id, recipient });
        // `transfer::transfer` is only callable from this module (key-only type).
        // No external code can ever invoke `public_transfer` here: missing `store`
        // makes the ability constraint fail at compile time, not runtime.
        transfer::transfer(badge, recipient);
    }

    /// The badge holder may voluntarily burn their badge.
    ///
    /// Because no external module can transfer a key-only object, burning is the
    /// only way to remove a badge from an address short of owning its private key.
    public fun burn(badge: Badge) {
        let badge_id = object::id(&badge);
        let Badge { id, recipient, name: _, description: _, issued_at_ms: _ } = badge;
        event::emit(BadgeBurned { badge_id, recipient });
        object::delete(id);
    }

    // ─── Read-only accessors (Move 2024 dot-notation compatible) ─────────────

    public fun name(self: &Badge): &vector<u8> { &self.name }
    public fun description(self: &Badge): &vector<u8> { &self.description }
    public fun recipient(self: &Badge): address { self.recipient }
    public fun issued_at_ms(self: &Badge): u64 { self.issued_at_ms }
}
