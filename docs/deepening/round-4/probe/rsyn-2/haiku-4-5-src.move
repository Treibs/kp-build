module steps::pedometer {
    public struct Pedometer has key, store {
        id: UID,
        today: u64,
        lifetime: u64,
    }

    public fun new_pedometer(ctx: &mut TxContext): Pedometer {
        Pedometer {
            id: object::new(ctx),
            today: 0,
            lifetime: 0,
        }
    }

    public fun log_steps(pedometer: &mut Pedometer, n: u64) {
        pedometer.today = pedometer.today + n;
    }

    public fun rollover(pedometer: &mut Pedometer): u64 {
        let day_count = pedometer.today;
        pedometer.lifetime = pedometer.lifetime + day_count;
        pedometer.today = 0;
        day_count
    }

    public fun lifetime_total(pedometer: &Pedometer): u64 {
        pedometer.lifetime + pedometer.today
    }
}
