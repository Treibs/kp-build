module toll::booth {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::event;
    use sui::balance::{Self, Balance};

    public struct TollBooth has key {
        id: UID,
        toll_amount: u64,
        balance: Balance<SUI>,
    }

    public struct OperatorCap has key, store {
        id: UID,
    }

    public struct TollPaid has copy, drop {
        payer: address,
        amount: u64,
    }

    public fun new(toll_amount: u64, ctx: &mut TxContext) {
        let booth = TollBooth {
            id: object::new(ctx),
            toll_amount,
            balance: balance::zero(),
        };
        let cap = OperatorCap {
            id: object::new(ctx),
        };
        transfer::share_object(booth);
        transfer::transfer(cap, ctx.sender());
    }

    public fun pay_toll(booth: &mut TollBooth, payment: Coin<SUI>, ctx: &mut TxContext) {
        let amount = coin::value(&payment);
        assert!(amount == booth.toll_amount, 0);
        
        let coin_balance = coin::into_balance(payment);
        balance::join(&mut booth.balance, coin_balance);
        
        let payer = ctx.sender();
        event::emit(TollPaid { payer, amount });
    }

    public fun sweep(_cap: &OperatorCap, booth: &mut TollBooth, max_amount: u64, ctx: &mut TxContext): Coin<SUI> {
        let available = balance::value(&booth.balance);
        let withdraw_amount = if (available > max_amount) {
            max_amount
        } else {
            available
        };
        
        let withdrawn = balance::split(&mut booth.balance, withdraw_amount);
        coin::from_balance(withdrawn, ctx)
    }
}
