module config::config {
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;
    use sui::transfer;

    public struct AdminCap has key, store {
        id: UID,
    }

    public struct Config has key, store {
        id: UID,
        fee_bps: u64,
        treasury: address,
    }

    fun init(ctx: &mut TxContext) {
        transfer::transfer(
            AdminCap {
                id: object::new(ctx),
            },
            ctx.sender(),
        );
    }

    public fun create(
        _cap: &AdminCap,
        fee_bps: u64,
        treasury: address,
        ctx: &mut TxContext,
    ): Config {
        Config {
            id: object::new(ctx),
            fee_bps,
            treasury,
        }
    }

    public fun set_fee_bps(config: &mut Config, _cap: &AdminCap, fee_bps: u64) {
        config.fee_bps = fee_bps;
    }

    public fun set_treasury(config: &mut Config, _cap: &AdminCap, treasury: address) {
        config.treasury = treasury;
    }

    public fun publish(config: Config, _cap: &AdminCap) {
        transfer::freeze_object(config);
    }

    public fun fee(config: &Config): u64 {
        config.fee_bps
    }
}
