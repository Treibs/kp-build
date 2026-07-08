module kp_build::inactivity_vault {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::transfer;
    use sui::object::{Self, UID};
    use sui::tx_context::{Self, TxContext};

    public struct Vault has key {
        id: UID,
        balance: Coin<SUI>,
        owner: address,
        beneficiary: address,
        timeout_epochs: u64,
        last_checkin_epoch: u64,
    }

    public fun create(
        owner: address,
        beneficiary: address,
        timeout_epochs: u64,
        coin: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let current_epoch = tx_context::epoch(ctx);
        
        let vault = Vault {
            id: object::new(ctx),
            balance: coin,
            owner,
            beneficiary,
            timeout_epochs,
            last_checkin_epoch: current_epoch,
        };

        transfer::transfer(vault, owner);
    }

    public fun check_in(vault: &mut Vault, ctx: &mut TxContext) {
        assert!(tx_context::sender(ctx) == vault.owner, 0);
        let current_epoch = tx_context::epoch(ctx);
        assert!(current_epoch - vault.last_checkin_epoch <= vault.timeout_epochs, 1);
        vault.last_checkin_epoch = current_epoch;
    }

    public fun deposit(vault: &mut Vault, coin: Coin<SUI>, ctx: &mut TxContext) {
        assert!(tx_context::sender(ctx) == vault.owner, 0);
        let current_epoch = tx_context::epoch(ctx);
        assert!(current_epoch - vault.last_checkin_epoch <= vault.timeout_epochs, 1);
        coin::join(&mut vault.balance, coin);
    }

    public fun withdraw(
        vault: &mut Vault,
        amount: u64,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        assert!(tx_context::sender(ctx) == vault.owner, 0);
        let current_epoch = tx_context::epoch(ctx);
        assert!(current_epoch - vault.last_checkin_epoch <= vault.timeout_epochs, 1);
        coin::split(&mut vault.balance, amount, ctx)
    }

    public fun claim(vault: Vault, ctx: &mut TxContext) {
        assert!(tx_context::sender(ctx) == vault.beneficiary, 2);
        let current_epoch = tx_context::epoch(ctx);
        assert!(current_epoch - vault.last_checkin_epoch > vault.timeout_epochs, 3);

        let Vault { id, balance, owner: _, beneficiary, timeout_epochs: _, last_checkin_epoch: _ } = vault;
        object::delete(id);
        transfer::public_transfer(balance, beneficiary);
    }
}
