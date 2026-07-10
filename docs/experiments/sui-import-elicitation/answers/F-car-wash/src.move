module wash_station::wash {
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::object::{Self, UID};
    use sui::sui::SUI;
    use sui::transfer;
    use sui::tx_context;

    const EInsufficientBalance: u64 = 0;

    public struct WashCard has key, store {
        id: UID,
        balance: Balance<SUI>,
    }

    public struct Station has key {
        id: UID,
        pool: Balance<SUI>,
        price_per_wash: u64,
    }

    public struct AdminCap has key, store {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        let admin = AdminCap {
            id: object::new(ctx),
        };
        transfer::transfer(admin, tx_context::sender(ctx));

        let station = Station {
            id: object::new(ctx),
            pool: balance::zero(),
            price_per_wash: 1_000_000,
        };
        transfer::share_object(station);
    }

    public fun new_card(ctx: &mut TxContext): WashCard {
        WashCard {
            id: object::new(ctx),
            balance: balance::zero(),
        }
    }

    public fun load(card: &mut WashCard, payment: Coin<SUI>) {
        balance::join(&mut card.balance, coin::into_balance(payment));
    }

    public fun wash(card: &mut WashCard, station: &mut Station) {
        assert!(balance::value(&card.balance) >= station.price_per_wash, EInsufficientBalance);
        let cost = balance::split(&mut card.balance, station.price_per_wash);
        balance::join(&mut station.pool, cost);
    }

    public fun sweep(
        station: &mut Station,
        _admin: &AdminCap,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let total = balance::value(&station.pool);
        let withdrawn = balance::split(&mut station.pool, total);
        coin::from_balance(withdrawn, ctx)
    }

    public fun card_balance(card: &WashCard): u64 {
        balance::value(&card.balance)
    }

    public fun set_price(_admin: &AdminCap, station: &mut Station, new_price: u64) {
        station.price_per_wash = new_price;
    }
}
