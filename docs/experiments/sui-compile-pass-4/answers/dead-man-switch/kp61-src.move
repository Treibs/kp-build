module inactivity_vault::vault {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::transfer;

    public struct Vault has key {
        id: UID,
        balance: Coin<SUI>,
        owner: address,
        beneficiary: address,
        timeout_epochs: u64,
        last_checkin_epoch: u64,
        active: bool,
    }

    public fun create(
        beneficiary: address,
        timeout_epochs: u64,
        coin: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let current_epoch = ctx.epoch();
        let vault = Vault {
            id: object::new(ctx),
            balance: coin,
            owner: ctx.sender(),
            beneficiary,
            timeout_epochs,
            last_checkin_epoch: current_epoch,
            active: true,
        };
        transfer::share_object(vault);
    }

    public fun check_in(vault: &mut Vault, ctx: &mut TxContext) {
        assert!(ctx.sender() == vault.owner);
        assert!(vault.active);
        vault.last_checkin_epoch = ctx.epoch();
    }

    public fun deposit(vault: &mut Vault, coin: Coin<SUI>, ctx: &mut TxContext) {
        assert!(ctx.sender() == vault.owner);
        assert!(vault.active);
        coin::join(&mut vault.balance, coin);
    }

    public fun withdraw(vault: &mut Vault, amount: u64, ctx: &mut TxContext): Coin<SUI> {
        assert!(ctx.sender() == vault.owner);
        assert!(vault.active);
        assert!(ctx.epoch() <= vault.last_checkin_epoch + vault.timeout_epochs);
        coin::split(&mut vault.balance, amount, ctx)
    }

    public fun claim(vault: &mut Vault, ctx: &mut TxContext): Coin<SUI> {
        assert!(ctx.sender() == vault.beneficiary);
        assert!(vault.active);
        assert!(ctx.epoch() > vault.last_checkin_epoch + vault.timeout_epochs);
        
        vault.active = false;
        let balance = coin::value(&vault.balance);
        coin::split(&mut vault.balance, balance, ctx)
    }
}
