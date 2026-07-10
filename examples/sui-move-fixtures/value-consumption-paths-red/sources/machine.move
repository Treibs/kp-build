module value_consumption_paths_red::machine {
    use sui::sui::SUI;
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};

    public struct Machine has key {
        id: UID,
        pool: Balance<SUI>,
        high: u64,
    }

    // the else path never consumes `payment` — a Coin has no drop, so
    // the happy-path-only branch fails to compile
    public fun play(m: &mut Machine, payment: Coin<SUI>, score: u64) {
        if (score > m.high) {
            m.high = score;
            coin::put(&mut m.pool, payment);
        }
    }

    public fun pool_value(m: &Machine): u64 {
        balance::value(&m.pool)
    }
}
