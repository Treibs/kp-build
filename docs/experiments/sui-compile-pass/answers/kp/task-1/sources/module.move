module shared_counter::counter {
    use sui::event;

    // Shared counter object — lives on-chain, accessible to everyone.
    public struct Counter has key {
        id: UID,
        value: u64,
    }

    // Capability minted to the deployer in `init`.
    // Possession of this object is the only authorisation needed to call `reset`.
    public struct AdminCap has key, store {
        id: UID,
    }

    // Events — must carry both `copy` and `drop` (emit<T: copy + drop> constraint).
    public struct Incremented has copy, drop {
        new_value: u64,
    }

    public struct Reset has copy, drop {}

    // `init` signature: no OTW needed here, so plain (ctx) form is correct.
    // UID, object, transfer, TxContext are all implicitly imported in edition 2024.
    fun init(ctx: &mut TxContext) {
        // Transfer the capability to the deployer; we are in the defining module
        // so transfer::transfer (T: key) is available without store.
        let admin_cap = AdminCap { id: object::new(ctx) };
        transfer::transfer(admin_cap, ctx.sender());

        // Share the counter so any transaction can pass it as a mutable argument.
        let counter = Counter { id: object::new(ctx), value: 0 };
        transfer::share_object(counter);
    }

    // Anyone can increment — no capability required.
    public fun increment(counter: &mut Counter) {
        counter.value = counter.value + 1;
        event::emit(Incremented { new_value: counter.value });
    }

    // Only the AdminCap holder can reset. Capability possession IS the auth check.
    public fun reset(counter: &mut Counter, _cap: &AdminCap) {
        counter.value = 0;
        event::emit(Reset {});
    }

    // Read-only accessor; callable via method syntax as `counter.value()`.
    public fun value(self: &Counter): u64 {
        self.value
    }
}
