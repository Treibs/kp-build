module casino::chip_tray {
    use sui::balance::{Balance, self};
    use sui::coin::{Coin, self};
    use sui::sui::SUI;
    use sui::event;

    public struct CashierCap has key, store {
        id: UID,
    }

    public struct ChipTray has key, store {
        id: UID,
        chips: Balance<SUI>,
        dealer: Option<address>,
    }

    public struct CasinoBank has key {
        id: UID,
        bankroll: Balance<SUI>,
        trays_prepared: u64,
        trays_assigned: u64,
    }

    public struct TrayPrepared has copy, drop {
        tray_id: ID,
    }

    public struct TrayAssigned has copy, drop {
        tray_id: ID,
        dealer: address,
    }

    public struct TrayScrapped has copy, drop {
        tray_id: ID,
        amount: u64,
    }

    fun init(ctx: &mut TxContext) {
        let cap = CashierCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, ctx.sender());
        
        let bank = CasinoBank {
            id: object::new(ctx),
            bankroll: balance::zero(),
            trays_prepared: 0,
            trays_assigned: 0,
        };
        transfer::share_object(bank);
    }

    public fun deposit_bankroll(
        _cap: &CashierCap,
        bank: &mut CasinoBank,
        funds: Coin<SUI>,
    ) {
        balance::join(&mut bank.bankroll, funds.into_balance());
    }

    public fun prepare_empty_tray(
        _cap: &CashierCap,
        bank: &mut CasinoBank,
        ctx: &mut TxContext,
    ): ChipTray {
        bank.trays_prepared = bank.trays_prepared + 1;
        
        let tray = ChipTray {
            id: object::new(ctx),
            chips: balance::zero(),
            dealer: option::none(),
        };
        
        event::emit(TrayPrepared {
            tray_id: object::uid_to_inner(&tray.id),
        });
        
        tray
    }

    public fun fill_tray_from_bankroll(
        _cap: &CashierCap,
        bank: &mut CasinoBank,
        tray: &mut ChipTray,
        amount: u64,
    ) {
        let chips = balance::split(&mut bank.bankroll, amount);
        balance::join(&mut tray.chips, chips);
    }

    public fun assign_tray_to_dealer(
        _cap: &CashierCap,
        bank: &mut CasinoBank,
        tray: &mut ChipTray,
        dealer: address,
    ) {
        option::fill(&mut tray.dealer, dealer);
        bank.trays_assigned = bank.trays_assigned + 1;
        
        event::emit(TrayAssigned {
            tray_id: object::uid_to_inner(&tray.id),
            dealer,
        });
    }

    public fun scrap_unused_tray(
        _cap: &CashierCap,
        bank: &mut CasinoBank,
        tray: ChipTray,
    ) {
        let ChipTray { id, chips, dealer: _ } = tray;
        let amount = chips.value();
        
        balance::join(&mut bank.bankroll, chips);
        
        event::emit(TrayScrapped {
            tray_id: object::uid_to_inner(&id),
            amount,
        });
        
        object::delete(id);
    }

    public fun view_prepared_trays(bank: &CasinoBank): u64 {
        bank.trays_prepared
    }

    public fun view_assigned_trays(bank: &CasinoBank): u64 {
        bank.trays_assigned
    }
}
