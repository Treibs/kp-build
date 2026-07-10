module laundromat::washer {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;

    public struct Washer has key {
        id: UID,
        price: u64,
        busy: bool,
        last_epoch: u64,
        balance: Coin<SUI>,
    }

    public struct OwnerCap has key, store {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        let washer = Washer {
            id: object::new(ctx),
            price: 1_000_000_000,
            busy: false,
            last_epoch: tx_context::epoch(ctx),
            balance: coin::zero<SUI>(ctx),
        };

        let owner_cap = OwnerCap {
            id: object::new(ctx),
        };

        transfer::share_object(washer);
        transfer::transfer(owner_cap, tx_context::sender(ctx));
    }

    public fun start_cycle(
        washer: &mut Washer,
        payment: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let current_epoch = tx_context::epoch(ctx);
        assert!(!washer.busy, 1);
        assert!(current_epoch > washer.last_epoch, 2);
        assert!(coin::value(&payment) == washer.price, 3);

        washer.busy = true;
        washer.last_epoch = current_epoch;
        coin::join(&mut washer.balance, payment);
    }

    public fun end_cycle(washer: &mut Washer) {
        assert!(washer.busy, 4);
        washer.busy = false;
    }

    public fun sweep(
        washer: &mut Washer,
        _cap: &OwnerCap,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let amount = coin::value(&washer.balance);
        coin::split(&mut washer.balance, amount, ctx)
    }
}
