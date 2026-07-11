module 0x0::sauna {
    use sui::object::{Self, UID};
    use sui::tx_context::{Self, TxContext};
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::transfer;
    use sui::event;

    public struct AdminCap has key, store {
        id: UID,
    }

    public struct Sauna has key {
        id: UID,
        price: u64,
        takings: Balance<SUI>,
        sessions_sold: u64,
        watcher: Option<address>,
        owner: address,
    }

    public struct SessionBought has copy, drop {
        sessions_sold: u64,
        amount_paid: u64,
        change_returned: u64,
    }

    public struct WatcherSet has copy, drop {
        watcher: Option<address>,
    }

    fun init(ctx: &mut TxContext) {
        let sender = tx_context::sender(ctx);
        
        let admin_cap = AdminCap {
            id: object::new(ctx),
        };
        
        let sauna = Sauna {
            id: object::new(ctx),
            price: 100_000_000,
            takings: balance::zero(),
            sessions_sold: 0,
            watcher: option::none(),
            owner: sender,
        };
        
        transfer::transfer(admin_cap, sender);
        transfer::share_object(sauna);
    }

    public fun set_watcher(sauna: &mut Sauna, watcher: Option<address>, _cap: &AdminCap) {
        sauna.watcher = watcher;
        event::emit(WatcherSet { watcher });
    }

    public fun buy_session(sauna: &mut Sauna, mut payment: Coin<SUI>, ctx: &mut TxContext): Coin<SUI> {
        assert!(option::is_some(&sauna.watcher), 1);
        
        let amount_paid = coin::value(&payment);
        assert!(amount_paid >= sauna.price, 2);
        
        let change_amount = amount_paid - sauna.price;
        
        let price_coin = coin::split(&mut payment, sauna.price, ctx);
        coin::put(&mut sauna.takings, price_coin);
        
        sauna.sessions_sold = sauna.sessions_sold + 1;
        
        event::emit(SessionBought {
            sessions_sold: sauna.sessions_sold,
            amount_paid,
            change_returned: change_amount,
        });
        
        payment
    }

    public fun sweep(sauna: &mut Sauna, _cap: &AdminCap, ctx: &mut TxContext): Coin<SUI> {
        let balance_withdrawn = balance::withdraw_all(&mut sauna.takings);
        coin::from_balance(balance_withdrawn, ctx)
    }

    public fun current_watcher(sauna: &Sauna): Option<address> {
        sauna.watcher
    }

    public fun sessions_sold(sauna: &Sauna): u64 {
        sauna.sessions_sold
    }

    public fun takings(sauna: &Sauna): u64 {
        balance::value(&sauna.takings)
    }
}
