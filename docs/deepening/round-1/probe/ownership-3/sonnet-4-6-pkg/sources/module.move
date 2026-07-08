module config::config;

public struct AdminCap has key, store {
    id: UID,
}

public struct Config has key {
    id: UID,
    fee_bps: u64,
    treasury: address,
}

fun init(ctx: &mut TxContext) {
    transfer::transfer(AdminCap { id: object::new(ctx) }, ctx.sender());
}

public fun create(_cap: &AdminCap, fee_bps: u64, treasury: address, ctx: &mut TxContext) {
    let config = Config {
        id: object::new(ctx),
        fee_bps,
        treasury,
    };
    transfer::transfer(config, ctx.sender());
}

public fun set_fee_bps(_cap: &AdminCap, config: &mut Config, fee_bps: u64) {
    config.fee_bps = fee_bps;
}

public fun set_treasury(_cap: &AdminCap, config: &mut Config, treasury: address) {
    config.treasury = treasury;
}

public fun publish(_cap: &AdminCap, config: Config) {
    transfer::freeze_object(config);
}

public fun fee_bps(config: &Config): u64 {
    config.fee_bps
}

public fun treasury(config: &Config): address {
    config.treasury
}
