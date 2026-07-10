module 0x0::change_machine {
    use sui::coin::{Coin, Self};
    use sui::sui::SUI;
    use sui::transfer;
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;
    use sui::balance::{Balance, Self};

    public struct ChangeMachine has key {
        id: UID,
        fees: Balance<SUI>,
    }

    public struct AdminCap has key, store {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        let machine = ChangeMachine {
            id: object::new(ctx),
            fees: balance::zero(),
        };
        transfer::share_object(machine);

        let admin = AdminCap {
            id: object::new(ctx),
        };
        transfer::transfer(admin, ctx.sender());
    }

    public fun exchange(
        machine: &mut ChangeMachine,
        mut coin: Coin<SUI>,
        denomination: u64,
        ctx: &mut TxContext,
    ): vector<Coin<SUI>> {
        let total_amount = coin::value(&coin);
        let num_coins = total_amount / denomination;
        let remainder = total_amount % denomination;

        let remainder_coin = coin::split(&mut coin, remainder, ctx);
        balance::join(&mut machine.fees, coin::into_balance(remainder_coin));

        let mut result = vector[];
        let mut i = 0;
        while (i < num_coins - 1) {
            let new_coin = coin::split(&mut coin, denomination, ctx);
            result.push_back(new_coin);
            i = i + 1;
        };

        result.push_back(coin);
        result
    }

    public fun sweep(_cap: &AdminCap, machine: &mut ChangeMachine, ctx: &mut TxContext): Coin<SUI> {
        let amount = balance::value(&machine.fees);
        let fees_balance = balance::split(&mut machine.fees, amount);
        coin::from_balance(fees_balance, ctx)
    }
}
