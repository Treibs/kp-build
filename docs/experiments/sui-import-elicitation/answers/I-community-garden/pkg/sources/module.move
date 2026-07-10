module garden::registry {
    use std::string::{Self, String};
    use sui::coin::{Self, Coin, SUI};
    use sui::balance::{Self, Balance, zero, join, withdraw};
    use sui::table::{Self, Table, new, add, remove, borrow_mut};
    use sui::event;

    public struct Garden has key {
        id: UID,
        plots: Table<u64, PlotData>,
        next_plot: u64,
        season_fee: u64,
        collected: Balance<SUI>,
    }

    public struct PlotData has store {
        plot_number: u64,
        owner: address,
        crop: String,
    }

    public struct AdminCap has key, store {
        id: UID,
    }

    public struct PlotClaimed has copy, drop {
        plot_number: u64,
        owner: address,
    }

    fun init(ctx: &mut TxContext) {
        let garden = Garden {
            id: object::new(ctx),
            plots: table::new(ctx),
            next_plot: 1,
            season_fee: 1_000_000_000,
            collected: balance::zero(),
        };
        
        let admin_cap = AdminCap {
            id: object::new(ctx),
        };
        
        transfer::share_object(garden);
        transfer::transfer(admin_cap, ctx.sender());
    }

    public fun claim_plot(
        garden: &mut Garden,
        payment: Coin<SUI>,
        ctx: &mut TxContext,
    ): u64 {
        let fee = garden.season_fee;
        assert!(coin::value(&payment) >= fee, EInsufficientFee);
        
        let plot_number = garden.next_plot;
        garden.next_plot = plot_number + 1;
        
        let plot = PlotData {
            plot_number,
            owner: ctx.sender(),
            crop: string::utf8(b""),
        };
        
        table::add(&mut garden.plots, plot_number, plot);
        balance::join(&mut garden.collected, coin::into_balance(payment));
        
        event::emit(PlotClaimed { plot_number, owner: ctx.sender() });
        plot_number
    }

    public fun plant(
        garden: &mut Garden,
        plot_number: u64,
        crop: String,
        ctx: &mut TxContext,
    ) {
        let plot = table::borrow_mut(&mut garden.plots, plot_number);
        assert!(plot.owner == ctx.sender(), ENotOwner);
        plot.crop = crop;
    }

    public fun release_plot(
        garden: &mut Garden,
        plot_number: u64,
        ctx: &mut TxContext,
    ) {
        let plot = table::remove(&mut garden.plots, plot_number);
        assert!(plot.owner == ctx.sender(), ENotOwner);
    }

    public fun sweep_fees(
        _cap: &AdminCap,
        garden: &mut Garden,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let amount = balance::value(&garden.collected);
        let fees = balance::withdraw(&mut garden.collected, amount);
        coin::from_balance(fees, ctx)
    }

    const EInsufficientFee: u64 = 1;
    const ENotOwner: u64 = 2;
}
