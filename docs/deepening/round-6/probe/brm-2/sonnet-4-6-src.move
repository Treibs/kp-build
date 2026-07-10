module duty_free::checkout {
    use sui::sui::SUI;
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};

    /// Held by the customs authority; required to issue stamps.
    public struct AdminCap has key {
        id: UID,
    }

    /// Capability issued to a traveler by customs; proves tax-exempt status.
    public struct Stamp has key, store {
        id: UID,
    }

    /// Shared till: collects payments and counts issued stamps.
    public struct Till has key {
        id: UID,
        balance: Balance<SUI>,
        stamps_issued: u64,
    }

    fun init(ctx: &mut TxContext) {
        let admin = AdminCap { id: object::new(ctx) };
        let till = Till {
            id: object::new(ctx),
            balance: balance::zero<SUI>(),
            stamps_issued: 0,
        };
        transfer::share_object(till);
        transfer::transfer(admin, ctx.sender());
    }

    /// Customs authority issues a stamp to a traveler.
    public fun issue_stamp(
        _cap: &AdminCap,
        till: &mut Till,
        recipient: address,
        ctx: &mut TxContext,
    ) {
        let stamp = Stamp { id: object::new(ctx) };
        till.stamps_issued = till.stamps_issued + 1;
        transfer::public_transfer(stamp, recipient);
    }

    /// Stamp holder pays the base price; surplus returned as change.
    public fun pay_with_stamp(
        till: &mut Till,
        _stamp: &Stamp,
        payment: Coin<SUI>,
        base_price: u64,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        assert!(coin::value(&payment) >= base_price);
        let mut bal = coin::into_balance(payment);
        let owed = balance::split(&mut bal, base_price);
        balance::join(&mut till.balance, owed);
        coin::from_balance(bal, ctx)
    }

    /// Non-stamp traveler pays base price + 20% tax; surplus returned as change.
    public fun pay(
        till: &mut Till,
        payment: Coin<SUI>,
        base_price: u64,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let total = base_price * 6 / 5;
        assert!(coin::value(&payment) >= total);
        let mut bal = coin::into_balance(payment);
        let owed = balance::split(&mut bal, total);
        balance::join(&mut till.balance, owed);
        coin::from_balance(bal, ctx)
    }

    /// Total MIST collected in the till.
    public fun till_total(till: &Till): u64 {
        balance::value(&till.balance)
    }

    /// Number of stamps that have been issued.
    public fun stamps_issued(till: &Till): u64 {
        till.stamps_issued
    }
}
