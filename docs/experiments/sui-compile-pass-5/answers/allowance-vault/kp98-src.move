module vault::vault {
    use sui::balance::{Balance, Self};
    use sui::coin::{Coin, Self};
    use sui::transfer;
    use sui::object::Self;
    use sui::tx_context::Self;
    use std::option::{Option, Self};
    use sui::clock::Clock;

    public struct OwnerCap has key, store {
        id: UID,
    }

    public struct Allowance has store {
        spender: address,
        limit_per_epoch: u64,
        current_epoch: u64,
        spent_this_epoch: u64,
    }

    public struct Vault has key {
        id: UID,
        balance: Balance<SUI>,
        allowance: Option<Allowance>,
    }

    public fun create(ctx: &mut TxContext): OwnerCap {
        let vault = Vault {
            id: object::new(ctx),
            balance: balance::zero(),
            allowance: option::none(),
        };
        transfer::share_object(vault);

        OwnerCap {
            id: object::new(ctx),
        }
    }

    public fun deposit(vault: &mut Vault, coin: Coin<SUI>) {
        balance::join(&mut vault.balance, coin::into_balance(coin));
    }

    public fun set_allowance(
        vault: &mut Vault,
        _cap: &OwnerCap,
        spender: address,
        limit_per_epoch: u64,
        clock: &Clock,
    ) {
        let epoch = get_epoch(clock);
        let new_allowance = Allowance {
            spender,
            limit_per_epoch,
            current_epoch: epoch,
            spent_this_epoch: 0,
        };

        if (option::is_some(&vault.allowance)) {
            let _ = option::extract(&mut vault.allowance);
        };
        option::fill(&mut vault.allowance, new_allowance);
    }

    public fun clear_allowance(vault: &mut Vault, _cap: &OwnerCap) {
        if (option::is_some(&vault.allowance)) {
            let _ = option::extract(&mut vault.allowance);
        };
    }

    public fun withdraw_as_owner(
        vault: &mut Vault,
        _cap: &OwnerCap,
        amount: u64,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let balance_out = balance::split(&mut vault.balance, amount);
        coin::from_balance(balance_out, ctx)
    }

    public fun withdraw_as_spender(
        vault: &mut Vault,
        amount: u64,
        clock: &Clock,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        assert!(option::is_some(&vault.allowance), 0);

        let allowance = option::borrow_mut(&mut vault.allowance);
        assert!(allowance.spender == ctx.sender(), 1);

        let epoch = get_epoch(clock);
        if (allowance.current_epoch < epoch) {
            allowance.current_epoch = epoch;
            allowance.spent_this_epoch = 0;
        };

        let new_spent = allowance.spent_this_epoch + amount;
        assert!(new_spent <= allowance.limit_per_epoch, 2);

        allowance.spent_this_epoch = new_spent;

        let balance_out = balance::split(&mut vault.balance, amount);
        coin::from_balance(balance_out, ctx)
    }

    fun get_epoch(clock: &Clock): u64 {
        clock.timestamp_ms() / 3600000
    }
}
