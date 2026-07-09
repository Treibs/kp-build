module toll::booth {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};
    use sui::event;

    public struct TollBooth has key {
        id: UID,
        toll: u64,
        balance: Balance<SUI>,
    }

    public struct OperatorCap has key, store {
        id: UID,
    }

    public struct TollPaid has copy, drop {
        payer: address,
        amount: u64,
    }

    public fun create(toll: u64, ctx: &mut TxContext): OperatorCap {
        let booth = TollBooth {
            id: object::new(ctx),
            toll,
            balance: balance::zero(),
        };
        transfer::share_object(booth);
        OperatorCap { id: object::new(ctx) }
    }

    public fun pay_toll(booth: &mut TollBooth, payment: Coin<SUI>, ctx: &TxContext) {
        assert!(payment.value() == booth.toll);
        let payer = ctx.sender();
        let amount = booth.toll;
        coin::put(&mut booth.balance, payment);
        event::emit(TollPaid { payer, amount });
    }

    public fun sweep(
        _cap: &OperatorCap,
        booth: &mut TollBooth,
        max_amount: u64,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let available = booth.balance.value();
        let withdraw = if (available < max_amount) { available } else { max_amount };
        coin::take(&mut booth.balance, withdraw, ctx)
    }
}
