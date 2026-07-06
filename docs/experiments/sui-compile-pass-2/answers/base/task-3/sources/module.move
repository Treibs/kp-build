module vault::vault {
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::object::{Self, UID};
    use sui::tx_context::{Self, TxContext};
    use sui::transfer;

    // ── Structs ───────────────────────────────────────────────────────────────

    /// Capability granting withdrawal rights over any `Vault` in this module.
    public struct AdminCap has key, store {
        id: UID,
    }

    /// Generic vault that holds a `Balance<T>` for any coin type `T`.
    /// Shared so any sender can deposit; only `AdminCap` holder can withdraw.
    public struct Vault<phantom T> has key {
        id: UID,
        balance: Balance<T>,
    }

    // ── Initialisation ────────────────────────────────────────────────────────

    /// Create a shared `Vault<T>` and send an `AdminCap` to the transaction
    /// sender.  Call once per coin type you want to vault.
    public entry fun create<T>(ctx: &mut TxContext) {
        let cap = AdminCap { id: object::new(ctx) };
        let vault = Vault<T> {
            id: object::new(ctx),
            balance: balance::zero<T>(),
        };
        transfer::transfer(cap, tx_context::sender(ctx));
        transfer::share_object(vault);
    }

    // ── Mutations ─────────────────────────────────────────────────────────────

    /// Deposit a `Coin<T>` into the vault.  Open to any caller.
    /// The coin is consumed and its value is merged into the stored balance.
    public fun deposit<T>(vault: &mut Vault<T>, coin: Coin<T>) {
        let incoming = coin::into_balance(coin);
        balance::join(&mut vault.balance, incoming);
    }

    /// Withdraw `amount` units from the vault as a `Coin<T>`.
    /// The caller must present the `AdminCap`; the cap is only checked by
    /// reference and is not consumed.
    public fun withdraw<T>(
        vault: &mut Vault<T>,
        _cap: &AdminCap,
        amount: u64,
        ctx: &mut TxContext,
    ): Coin<T> {
        let withdrawn = balance::split(&mut vault.balance, amount);
        coin::from_balance(withdrawn, ctx)
    }

    // ── Reads ─────────────────────────────────────────────────────────────────

    /// Return the current stored balance value (in base units).
    public fun balance<T>(vault: &Vault<T>): u64 {
        balance::value(&vault.balance)
    }
}
