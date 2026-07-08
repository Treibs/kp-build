module 0x0::vault {
    use std::option::{Self, Option};
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::clock::Clock;

    const EPOCH_DURATION_MS: u64 = 86400000;

    public struct Vault has key {
        id: UID,
        balance: Balance<SUI>,
        allowance: Option<Allowance>,
    }

    public struct Allowance has store {
        spender: address,
        per_epoch_limit: u64,
        spent_this_epoch: u64,
        last_reset_timestamp: u64,
    }

    public struct OwnerCap has key, store {
        id: UID,
        vault_id: ID,
    }

    public fun create_vault(coin: Coin<SUI>, ctx: &mut TxContext) -> OwnerCap {
        let vault = Vault {
            id: object::new(ctx),
            balance: coin::into_balance(coin),
            allowance: option::none(),
        };
        let vault_id = object::id(&vault);
        transfer::share_object(vault);
        OwnerCap {
            id: object::new(ctx),
            vault_id,
        }
    }

    public fun set_allowance(
        cap: &OwnerCap,
        vault: &mut Vault,
        spender: address,
        per_epoch_limit: u64,
        clock: &Clock,
    ) {
        assert!(cap.vault_id == object::id(vault));
        let allowance = Allowance {
            spender,
            per_epoch_limit,
            spent_this_epoch: 0,
            last_reset_timestamp: clock.timestamp_ms(),
        };
        vault.allowance = option::some(allowance);
    }

    public fun clear_allowance(cap: &OwnerCap, vault: &mut Vault) {
        assert!(cap.vault_id == object::id(vault));
        vault.allowance = option::none();
    }

    public fun spender_withdraw(
        vault: &mut Vault,
        amount: u64,
        clock: &Clock,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let allowance = option::borrow_mut(&mut vault.allowance);
        assert!(allowance.spender == ctx.sender());
        
        let current_timestamp = clock.timestamp_ms();
        if (current_timestamp >= allowance.last_reset_timestamp + EPOCH_DURATION_MS) {
            allowance.spent_this_epoch = 0;
            allowance.last_reset_timestamp = current_timestamp;
        }

        assert!(allowance.spent_this_epoch + amount <= allowance.per_epoch_limit);
        allowance.spent_this_epoch = allowance.spent_this_epoch + amount;

        coin::from_balance(
            balance::split(&mut vault.balance, amount),
            ctx,
        )
    }

    public fun owner_withdraw(
        cap: &OwnerCap,
        vault: &mut Vault,
        amount: u64,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        assert!(cap.vault_id == object::id(vault));
        coin::from_balance(
            balance::split(&mut vault.balance, amount),
            ctx,
        )
    }
}
