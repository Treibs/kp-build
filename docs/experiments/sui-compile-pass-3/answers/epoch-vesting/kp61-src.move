module vesting::wallet {
    use sui::coin::{Coin, split};
    use sui::sui::SUI;

    public struct Wallet has key, store {
        id: UID,
        beneficiary: address,
        balance: Coin<SUI>,
        start_epoch: u64,
        duration_epochs: u64,
        claimed: u64,
    }

    public fun create(
        beneficiary: address,
        start_epoch: u64,
        duration_epochs: u64,
        amount: Coin<SUI>,
        ctx: &mut TxContext,
    ): Wallet {
        Wallet {
            id: object::new(ctx),
            beneficiary,
            balance: amount,
            start_epoch,
            duration_epochs,
            claimed: 0,
        }
    }

    public fun claim(
        wallet: &mut Wallet,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        assert!(ctx.sender() == wallet.beneficiary);
        
        let current_epoch = ctx.epoch();
        let total_amount = wallet.balance.value() + wallet.claimed;
        
        let vested = if (current_epoch < wallet.start_epoch) {
            0
        } else if (current_epoch >= wallet.start_epoch + wallet.duration_epochs) {
            total_amount
        } else {
            let elapsed = current_epoch - wallet.start_epoch;
            (total_amount * elapsed) / wallet.duration_epochs
        };

        let claimable = vested - wallet.claimed;
        wallet.claimed = vested;
        
        split(&mut wallet.balance, claimable, ctx)
    }
}
