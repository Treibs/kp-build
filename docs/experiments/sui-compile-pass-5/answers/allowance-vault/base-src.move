module vault::delegated_vault {
    use sui::balance::{Balance, split};
    use sui::coin::{Coin, from_balance, into_balance};
    use sui::dynamic_object_field;
    use sui::object::{new, UID, ID, id};
    use sui::sui::SUI;
    use sui::transfer;
    use sui::tx_context::{TxContext, sender, epoch};

    public struct OwnerCap has key {
        id: UID,
        vault_id: ID,
    }

    public struct Vault has key {
        id: UID,
        balance: Balance<SUI>,
    }

    public struct Allowance has store {
        spender: address,
        per_epoch_limit: u64,
        current_epoch: u64,
        spent_this_epoch: u64,
    }

    public fun create_vault(coin: Coin<SUI>, ctx: &mut TxContext) {
        let vault = Vault {
            id: new(ctx),
            balance: into_balance(coin),
        };
        let owner_cap = OwnerCap {
            id: new(ctx),
            vault_id: id(&vault),
        };
        transfer::transfer(owner_cap, sender(ctx));
        transfer::share_object(vault);
    }

    public fun set_allowance(
        vault: &mut Vault,
        owner_cap: &OwnerCap,
        spender: address,
        per_epoch_limit: u64,
        ctx: &TxContext,
    ) {
        assert!(owner_cap.vault_id == id(vault), 0);
        
        let allowance = Allowance {
            spender,
            per_epoch_limit,
            current_epoch: epoch(ctx),
            spent_this_epoch: 0,
        };
        
        if (dynamic_object_field::exists_(&vault.id, 0u8)) {
            let _: Allowance = dynamic_object_field::remove(&mut vault.id, 0u8);
        };
        
        dynamic_object_field::add(&mut vault.id, 0u8, allowance);
    }

    public fun clear_allowance(
        vault: &mut Vault,
        owner_cap: &OwnerCap,
    ) {
        assert!(owner_cap.vault_id == id(vault), 0);
        
        if (dynamic_object_field::exists_(&vault.id, 0u8)) {
            let _: Allowance = dynamic_object_field::remove(&mut vault.id, 0u8);
        };
    }

    public fun spender_withdraw(
        vault: &mut Vault,
        amount: u64,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let allowance: &mut Allowance = dynamic_object_field::borrow_mut(&mut vault.id, 0u8);
        
        assert!(allowance.spender == sender(ctx), 1);
        
        let current_epoch = epoch(ctx);
        if (current_epoch > allowance.current_epoch) {
            allowance.spent_this_epoch = 0;
            allowance.current_epoch = current_epoch;
        };
        
        assert!(allowance.spent_this_epoch + amount <= allowance.per_epoch_limit, 2);
        
        allowance.spent_this_epoch = allowance.spent_this_epoch + amount;
        
        from_balance(split(&mut vault.balance, amount), ctx)
    }

    public fun owner_withdraw(
        vault: &mut Vault,
        owner_cap: &OwnerCap,
        amount: u64,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        assert!(owner_cap.vault_id == id(vault), 0);
        from_balance(split(&mut vault.balance, amount), ctx)
    }
}
