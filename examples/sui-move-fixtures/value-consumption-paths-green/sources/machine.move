module value_consumption_paths_green::machine {
    use sui::sui::SUI;
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};

    public struct Machine has key {
        id: UID,
        pool: Balance<SUI>,
        high: u64,
    }

    // a non-drop parameter must be consumed on EVERY path: the losing
    // branch hands the payment back to the caller instead of leaving it
    // unconsumed (composable — no transfer-to-sender)
    public fun play(m: &mut Machine, payment: Coin<SUI>, score: u64): Option<Coin<SUI>> {
        if (score > m.high) {
            m.high = score;
            coin::put(&mut m.pool, payment);
            option::none()
        } else {
            option::some(payment)
        }
    }

    public fun pool_value(m: &Machine): u64 {
        balance::value(&m.pool)
    }
}
