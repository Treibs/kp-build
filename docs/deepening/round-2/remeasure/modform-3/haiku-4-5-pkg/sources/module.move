module fee_splitter::payment {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;

    public struct FeeConfig has key, store {
        id: UID,
        fee_bps: u64,
        treasury: address,
    }

    public fun create_fee_config(fee_bps: u64, treasury: address, ctx: &mut TxContext) {
        let config = FeeConfig {
            id: object::new(ctx),
            fee_bps,
            treasury,
        };
        transfer::share_object(config);
    }

    entry fun pay(
        config: &FeeConfig,
        mut payment: Coin<SUI>,
        recipient: address,
        ctx: &mut TxContext,
    ) {
        let total_amount = coin::value(&payment);
        let fee_amount = (total_amount * config.fee_bps) / 10000;

        let fee_coin = coin::split(&mut payment, fee_amount, ctx);

        transfer::public_transfer(fee_coin, config.treasury);
        transfer::public_transfer(payment, recipient);
    }
}
