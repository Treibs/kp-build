module wishing_well::well {
    use sui::coin::{Coin};
    use sui::sui::SUI;
    use sui::balance::{Balance};
    use sui::coin;
    use sui::balance;
    use sui::event;

    public struct WishingWell has key {
        id: UID,
        total: u64,
        largest_wish: u64,
        balance: Balance<SUI>,
    }

    public struct KeeperCap has key, store {
        id: UID,
    }

    public struct WishMade has copy, drop {
        amount: u64,
        total: u64,
        largest: u64,
    }

    fun init(ctx: &mut TxContext) {
        let well = WishingWell {
            id: object::new(ctx),
            total: 0,
            largest_wish: 0,
            balance: balance::zero(),
        };

        let keeper = KeeperCap {
            id: object::new(ctx),
        };

        transfer::share_object(well);
        transfer::transfer(keeper, ctx.sender());
    }

    public fun make_wish(
        well: &mut WishingWell,
        coin_wish: Coin<SUI>,
    ) {
        let amount = coin::value(&coin_wish);
        assert!(amount > 0, 1);

        well.total = well.total + amount;
        if (amount > well.largest_wish) {
            well.largest_wish = amount;
        };

        let coin_balance = coin::into_balance(coin_wish);
        balance::join(&mut well.balance, coin_balance);

        event::emit(WishMade {
            amount,
            total: well.total,
            largest: well.largest_wish,
        });
    }

    public fun drain(
        well: &mut WishingWell,
        _cap: &KeeperCap,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let drained = balance::withdraw_all(&mut well.balance);
        coin::from_balance(drained, ctx)
    }

    public fun total(well: &WishingWell): u64 {
        well.total
    }

    public fun largest_wish(well: &WishingWell): u64 {
        well.largest_wish
    }
}
