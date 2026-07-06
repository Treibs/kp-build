module soulbound::badge {

    use std::string::{Self, String};

    // === Errors ===
    const ECannotTransfer: u64 = 0;

    // === Types ===

    /// A soulbound badge that is permanently bound to its recipient.
    /// The `key` ability allows it to be a Sui object.
    /// Notably, it does NOT have the `store` ability, which prevents
    /// it from being transferred via generic transfer functions or
    /// placed inside other objects by third parties.
    public struct Badge has key {
        id: UID,
        name: String,
        description: String,
        recipient: address,
        issued_at_epoch: u64,
    }

    /// Capability held by the issuer that grants permission to mint badges.
    public struct IssuerCap has key, store {
        id: UID,
    }

    // === Events ===

    public struct BadgeMinted has copy, drop {
        badge_id: ID,
        recipient: address,
        name: String,
    }

    // === Init ===

    /// Called once on package publish. Transfers the IssuerCap to the deployer.
    fun init(ctx: &mut TxContext) {
        let cap = IssuerCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, tx_context::sender(ctx));
    }

    // === Public Entry Functions ===

    /// Mint a new soulbound badge and deliver it directly to `recipient`.
    /// Only the holder of IssuerCap may call this.
    /// Because Badge lacks `store`, the only legal Sui transfer primitive
    /// available is `transfer::transfer` (single-owner, no wrapping),
    /// and that can only be called here in this module — callers outside
    /// the module cannot move the object anywhere.
    public entry fun mint(
        _cap: &IssuerCap,
        name: vector<u8>,
        description: vector<u8>,
        recipient: address,
        ctx: &mut TxContext,
    ) {
        let badge = Badge {
            id: object::new(ctx),
            name: string::utf8(name),
            description: string::utf8(description),
            recipient,
            issued_at_epoch: tx_context::epoch(ctx),
        };

        let badge_id = object::id(&badge);

        sui::event::emit(BadgeMinted {
            badge_id,
            recipient,
            name: badge.name,
        });

        // Deliver to the recipient. This is the ONLY place a Badge can
        // ever be transferred — there is no public transfer function,
        // and the missing `store` ability prevents all external moves.
        transfer::transfer(badge, recipient);
    }

    // === Read-only Accessors ===

    public fun name(badge: &Badge): &String {
        &badge.name
    }

    public fun description(badge: &Badge): &String {
        &badge.description
    }

    public fun recipient(badge: &Badge): address {
        badge.recipient
    }

    public fun issued_at_epoch(badge: &Badge): u64 {
        badge.issued_at_epoch
    }
}
