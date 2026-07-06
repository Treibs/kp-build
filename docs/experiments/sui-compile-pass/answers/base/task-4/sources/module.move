module escrow::atomic_swap {

    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};

    /// Error codes
    const ENotPartyA: u64 = 0;
    const ENotPartyB: u64 = 1;
    const EWrongObject: u64 = 2;
    const EAlreadyDeposited: u64 = 3;

    /// A held object wrapper that stores the deposited item and swap metadata.
    public struct EscrowedObject<T: key + store> has key {
        id: UID,
        /// The party who deposited this object
        depositor: address,
        /// The counterparty who should receive this object
        recipient: address,
        /// The ID of the object the depositor expects to receive in return
        exchange_for: address,
        /// The deposited object
        escrowed: T,
    }

    /// Deposit an object into escrow.
    /// - `recipient`: the address of the counterparty
    /// - `exchange_for`: the object ID (as address) that the depositor wants in return
    /// - `obj`: the object being deposited
    public fun create<T: key + store>(
        recipient: address,
        exchange_for: address,
        obj: T,
        ctx: &mut TxContext,
    ) {
        let depositor = tx_context::sender(ctx);
        let escrowed_obj = EscrowedObject<T> {
            id: object::new(ctx),
            depositor,
            recipient,
            exchange_for,
            escrowed: obj,
        };
        // Transfer the escrow wrapper to the recipient so they can complete the swap
        transfer::share_object(escrowed_obj);
    }

    /// Complete the swap.
    /// Party B calls this, providing the object that party A is expecting.
    /// Both objects are atomically exchanged.
    public fun swap<T: key + store, U: key + store>(
        escrow_a: EscrowedObject<T>,
        escrow_b: EscrowedObject<U>,
        ctx: &mut TxContext,
    ) {
        let sender = tx_context::sender(ctx);

        // Destructure escrow A
        let EscrowedObject {
            id: id_a,
            depositor: depositor_a,
            recipient: recipient_a,
            exchange_for: exchange_for_a,
            escrowed: obj_a,
        } = escrow_a;

        // Destructure escrow B
        let EscrowedObject {
            id: id_b,
            depositor: depositor_b,
            recipient: recipient_b,
            exchange_for: exchange_for_b,
            escrowed: obj_b,
        } = escrow_b;

        // Verify the swap is consistent:
        // escrow_a was deposited by A for B
        assert!(depositor_a == recipient_b, ENotPartyA);
        // escrow_b was deposited by B for A
        assert!(depositor_b == recipient_a, ENotPartyB);

        // Verify the objects match what each party requested
        assert!(
            exchange_for_a == object::id_address(&obj_b),
            EWrongObject
        );
        assert!(
            exchange_for_b == object::id_address(&obj_a),
            EWrongObject
        );

        // Caller must be one of the two parties
        assert!(sender == depositor_a || sender == depositor_b, ENotPartyB);

        // Delete the escrow wrapper UIDs
        object::delete(id_a);
        object::delete(id_b);

        // Atomically transfer each object to the respective counterparty
        transfer::public_transfer(obj_a, depositor_b);
        transfer::public_transfer(obj_b, depositor_a);
    }

    /// Cancel an escrow and reclaim the deposited object.
    /// Only the original depositor can cancel.
    public fun cancel<T: key + store>(
        escrow: EscrowedObject<T>,
        ctx: &mut TxContext,
    ) {
        let sender = tx_context::sender(ctx);
        let EscrowedObject {
            id,
            depositor,
            recipient: _,
            exchange_for: _,
            escrowed: obj,
        } = escrow;

        assert!(sender == depositor, ENotPartyA);

        object::delete(id);
        transfer::public_transfer(obj, depositor);
    }
}
