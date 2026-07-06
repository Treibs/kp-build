// Move 2024 edition — Sui mainnet toolchain (sui 1.74.x)
module vault::vault {
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};

    // -------------------------------------------------------------------------
    // Object types
    // -------------------------------------------------------------------------

    /// A generic vault that custodies `Balance<T>` on behalf of its admin.
    /// Published as a shared object so any party may call `deposit`;
    /// withdrawals are gated behind `AdminCap`.
    public struct Vault<phantom T> has key {
        id: UID,
        balance: Balance<T>,
    }

    /// Capability minted once in `init` and delivered to the package publisher.
    /// Presenting this object proves admin authority to `create` vaults and
    /// `withdraw` funds.
    public struct AdminCap has key, store {
        id: UID,
    }

    // -------------------------------------------------------------------------
    // Module initializer — runs exactly once at publish time
    // -------------------------------------------------------------------------

    /// Mint the sole `AdminCap` and transfer it to the publishing transaction
    /// sender.
    fun init(ctx: &mut TxContext) {
        let cap = AdminCap { id: object::new(ctx) };
        transfer::transfer(cap, ctx.sender());
    }

    // -------------------------------------------------------------------------
    // Vault lifecycle
    // -------------------------------------------------------------------------

    /// Create an empty `Vault<T>` and share it.  Guarded by `AdminCap` so
    /// only the admin can open new vaults.
    public fun create<T>(
        _cap: &AdminCap,
        ctx: &mut TxContext,
    ) {
        let vault = Vault<T> {
            id: object::new(ctx),
            balance: balance::zero<T>(),
        };
        transfer::share_object(vault);
    }

    // -------------------------------------------------------------------------
    // Deposit — open to any caller
    // -------------------------------------------------------------------------

    /// Convert `coin` into a raw `Balance<T>` and merge it into the vault.
    public fun deposit<T>(vault: &mut Vault<T>, coin: Coin<T>) {
        let incoming = coin::into_balance(coin);
        balance::join(&mut vault.balance, incoming);
    }

    // -------------------------------------------------------------------------
    // Withdraw — admin only
    // -------------------------------------------------------------------------

    /// Split `amount` units from the vault balance and wrap them in a
    /// `Coin<T>` that the caller can transfer to any recipient.
    /// Requires the `AdminCap` — possession of the cap IS the authorization.
    public fun withdraw<T>(
        _cap: &AdminCap,
        vault: &mut Vault<T>,
        amount: u64,
        ctx: &mut TxContext,
    ): Coin<T> {
        let split_balance = balance::split(&mut vault.balance, amount);
        coin::from_balance(split_balance, ctx)
    }

    // -------------------------------------------------------------------------
    // View
    // -------------------------------------------------------------------------

    /// Return the vault's current balance without consuming anything.
    public fun value<T>(vault: &Vault<T>): u64 {
        balance::value(&vault.balance)
    }
}
