module steps::pedometer {
    public struct Pedometer has key {
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

    public fun log_steps(self: &mut Pedometer, n: u64) {
        self.today = self.today + n;
    }

    public fun rollover(self: &mut Pedometer): u64 {
        let closed = self.today;
        self.lifetime = self.lifetime + closed;
        self.today = 0;
        closed
    }

    public fun lifetime_total(self: &Pedometer): u64 {
        self.lifetime + self.today
    }
}
