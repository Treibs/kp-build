module fee_split::payment {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;

    public struct FeeConfig has key {
        id: UID,
        fee_bps: u64,
        treasury: address,
    }

    public fun create_fee_config(fee_bps: u64, treasury: address, ctx: &mut TxContext) {
        transfer::share_object(FeeConfig {
            id: object::new(ctx),
            fee_bps,
            treasury,
        });
    }

    entry fun pay(
        config: &FeeConfig,
        mut payment: Coin<SUI>,
        recipient: address,
        ctx: &mut TxContext,
    ) {
        let total = coin::value(&payment);
        let fee_amount = total * config.fee_bps / 10000;
        let fee_coin = coin::split(&mut payment, fee_amount, ctx);
        transfer::public_transfer(fee_coin, config.treasury);
        transfer::public_transfer(payment, recipient);
    }
}
