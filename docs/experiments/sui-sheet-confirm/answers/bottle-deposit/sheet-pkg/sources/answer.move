module deposit_scheme {
    use sui::coin::{Coin, Self};
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};
    use sui::object::{Self, UID, ID};
    use sui::tx_context::TxContext;
    use sui::transfer;

    public struct Scheme has key, store {
        id: UID,
        deposit_amount: u64,
        reservoir: Balance<SUI>,
        sold_bottles: u64,
        returned_bottles: u64,
    }

    public struct DistributorCap has key, store {
        id: UID,
        scheme_id: ID,
    }

    public struct Bottle has key, store {
        id: UID,
        scheme_id: ID,
    }

    const EInvalidPayment: u64 = 1;
    const EDifferentScheme: u64 = 2;
    const EExcessiveWithdrawal: u64 = 3;
    const ECapMismatch: u64 = 4;

    public fun create_scheme(
        deposit_amount: u64,
        ctx: &mut TxContext,
    ): DistributorCap {
        let scheme = Scheme {
            id: object::new(ctx),
            deposit_amount,
            reservoir: balance::zero(),
            sold_bottles: 0,
            returned_bottles: 0,
        };

        let scheme_id = object::id(&scheme);

        let cap = DistributorCap {
            id: object::new(ctx),
            scheme_id,
        };

        transfer::share_object(scheme);
        cap
    }

    public fun sell_bottle(
        cap: &DistributorCap,
        scheme: &mut Scheme,
        payment: Coin<SUI>,
        ctx: &mut TxContext,
    ): Bottle {
        assert!(cap.scheme_id == object::id(scheme), ECapMismatch);
        assert!(coin::value(&payment) == scheme.deposit_amount, EInvalidPayment);
        
        balance::join(&mut scheme.reservoir, coin::into_balance(payment));
        scheme.sold_bottles += 1;

        Bottle {
            id: object::new(ctx),
            scheme_id: object::id(scheme),
        }
    }

    public fun return_bottle(
        scheme: &mut Scheme,
        bottle: Bottle,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let Bottle { id, scheme_id } = bottle;
        assert!(scheme_id == object::id(scheme), EDifferentScheme);
        
        object::delete(id);
        scheme.returned_bottles += 1;

        let refund = balance::split(&mut scheme.reservoir, scheme.deposit_amount);
        coin::from_balance(refund, ctx)
    }

    public fun top_up_reservoir(
        cap: &DistributorCap,
        scheme: &mut Scheme,
        payment: Coin<SUI>,
    ) {
        assert!(cap.scheme_id == object::id(scheme), ECapMismatch);
        balance::join(&mut scheme.reservoir, coin::into_balance(payment));
    }

    public fun withdraw_from_reservoir(
        cap: &DistributorCap,
        scheme: &mut Scheme,
        amount: u64,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        assert!(cap.scheme_id == object::id(scheme), ECapMismatch);
        
        let outstanding = outstanding_bottle_count(scheme);
        let min_reserve = outstanding * scheme.deposit_amount;
        let current_balance = balance::value(&scheme.reservoir);
        
        assert!(current_balance >= min_reserve + amount, EExcessiveWithdrawal);

        let withdrawal = balance::split(&mut scheme.reservoir, amount);
        coin::from_balance(withdrawal, ctx)
    }

    public fun outstanding_bottle_count(scheme: &Scheme): u64 {
        scheme.sold_bottles - scheme.returned_bottles
    }

    public fun reservoir_balance(scheme: &Scheme): u64 {
        balance::value(&scheme.reservoir)
    }
}
