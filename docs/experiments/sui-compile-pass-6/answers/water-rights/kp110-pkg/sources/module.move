module reservoir_ledger::reservoir {
    public struct AdminCap has key, store {
        id: UID,
    }

    public struct Reservoir has key, store {
        id: UID,
        balance: u64,
        epoch: u64,
    }

    public struct WaterRight has key, store {
        id: UID,
        holder: address,
        allocation_amount: u64,
        total_drawn_this_epoch: u64,
        epoch: u64,
    }

    fun init(ctx: &mut TxContext) {
        let admin_cap = AdminCap {
            id: object::new(ctx),
        };
        transfer::transfer(admin_cap, tx_context::sender(ctx));
    }

    public fun create_reservoir(_cap: &AdminCap, initial_balance: u64, ctx: &mut TxContext) {
        let reservoir = Reservoir {
            id: object::new(ctx),
            balance: initial_balance,
            epoch: 0,
        };
        transfer::share_object(reservoir);
    }

    public fun issue_water_right(
        _cap: &AdminCap,
        reservoir: &Reservoir,
        holder: address,
        allocation: u64,
        ctx: &mut TxContext,
    ) {
        let right = WaterRight {
            id: object::new(ctx),
            holder,
            allocation_amount: allocation,
            total_drawn_this_epoch: 0,
            epoch: reservoir.epoch,
        };
        transfer::transfer(right, holder);
    }

    public fun draw(
        reservoir: &mut Reservoir,
        right: &mut WaterRight,
        amount: u64,
        ctx: &TxContext,
    ) {
        assert!(tx_context::sender(ctx) == right.holder, 1);
        
        if (right.epoch < reservoir.epoch) {
            right.epoch = reservoir.epoch;
            right.total_drawn_this_epoch = 0;
        };
        
        assert!(right.total_drawn_this_epoch + amount <= right.allocation_amount, 2);
        assert!(reservoir.balance >= amount, 3);
        
        right.total_drawn_this_epoch = right.total_drawn_this_epoch + amount;
        reservoir.balance = reservoir.balance - amount;
    }

    public fun refill(_cap: &AdminCap, reservoir: &mut Reservoir, amount: u64) {
        reservoir.balance = reservoir.balance + amount;
    }

    public fun advance_epoch(_cap: &AdminCap, reservoir: &mut Reservoir) {
        reservoir.epoch = reservoir.epoch + 1;
    }

    public fun get_balance(reservoir: &Reservoir): u64 {
        reservoir.balance
    }

    public fun get_allocation(right: &WaterRight): u64 {
        right.allocation_amount
    }

    public fun get_drawn(right: &WaterRight): u64 {
        right.total_drawn_this_epoch
    }

    public fun get_epoch(reservoir: &Reservoir): u64 {
        reservoir.epoch
    }
}
