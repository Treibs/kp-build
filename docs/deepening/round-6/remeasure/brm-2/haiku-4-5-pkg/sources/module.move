module duty_free::checkout {
    use sui::coin::{self, Coin};
    use sui::sui::SUI;
    use sui::balance::{self, Balance};
    use std::option::{self, Option};

    public struct Stamp has key, store {
        id: UID,
    }

    public struct Till has key {
        id: UID,
        balance: Balance<SUI>,
        stamps_issued: u64,
    }

    fun init(ctx: &mut TxContext) {
        let till = Till {
            id: object::new(ctx),
            balance: balance::zero(),
            stamps_issued: 0,
        };
        transfer::share_object(till);
    }

    public fun issue_stamp(till: &mut Till, ctx: &mut TxContext) {
        let stamp = Stamp {
            id: object::new(ctx),
        };
        till.stamps_issued = till.stamps_issued + 1;
        transfer::transfer(stamp, ctx.sender());
    }

    public fun checkout(
        till: &mut Till,
        base_price: u64,
        mut payment: Coin<SUI>,
        stamp: Option<Stamp>,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let has_stamp = option::is_some(&stamp);
        
        let owed = if (has_stamp) {
            base_price
        } else {
            base_price + (base_price / 5)
        };

        assert!(coin::value(&payment) >= owed, 1);

        if (has_stamp) {
            let Stamp { id } = option::extract(&mut stamp);
            object::delete(id);
        };
        option::destroy_none(stamp);

        let owed_coin = coin::split(&mut payment, owed, ctx);
        balance::join(&mut till.balance, coin::into_balance(owed_coin));

        payment
    }

    public fun till_total(till: &Till): u64 {
        balance::value(&till.balance)
    }

    public fun stamps_issued(till: &Till): u64 {
        till.stamps_issued
    }
}
