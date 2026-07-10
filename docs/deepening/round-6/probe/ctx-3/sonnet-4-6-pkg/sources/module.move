module casino::floor {
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};
    use sui::sui::SUI;
    use std::string::String;

    const FILL_AMOUNT: u64 = 100_000_000;

    public struct CashierCap has key, store {
        id: UID,
    }

    public struct ChipTray has key, store {
        id: UID,
        chips: Balance<SUI>,
        dealer: Option<String>,
    }

    public struct FloorLedger has key {
        id: UID,
        trays_prepared: u64,
        trays_assigned: u64,
    }

    fun init(ctx: &mut TxContext) {
        transfer::transfer(
            CashierCap { id: object::new(ctx) },
            ctx.sender()
        );
        transfer::share_object(FloorLedger {
            id: object::new(ctx),
            trays_prepared: 0,
            trays_assigned: 0,
        });
    }

    public fun prepare_tray(
        _cap: &CashierCap,
        ledger: &mut FloorLedger,
        ctx: &mut TxContext,
    ): ChipTray {
        ledger.trays_prepared = ledger.trays_prepared + 1;
        ChipTray {
            id: object::new(ctx),
            chips: balance::zero(),
            dealer: option::none(),
        }
    }

    public fun fill_tray(
        _cap: &CashierCap,
        tray: &mut ChipTray,
        bankroll: &mut Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        assert!(balance::value(&tray.chips) == 0);
        assert!(option::is_none(&tray.dealer));
        let portion = coin::split(bankroll, FILL_AMOUNT, ctx);
        balance::join(&mut tray.chips, coin::into_balance(portion));
    }

    public fun assign_tray(
        _cap: &CashierCap,
        mut tray: ChipTray,
        dealer_name: String,
        dealer_addr: address,
        ledger: &mut FloorLedger,
    ) {
        assert!(balance::value(&tray.chips) == FILL_AMOUNT);
        assert!(option::is_none(&tray.dealer));
        option::fill(&mut tray.dealer, dealer_name);
        ledger.trays_assigned = ledger.trays_assigned + 1;
        transfer::transfer(tray, dealer_addr);
    }

    public fun scrap_tray(_cap: &CashierCap, tray: ChipTray) {
        assert!(balance::value(&tray.chips) == 0);
        assert!(option::is_none(&tray.dealer));
        let ChipTray { id, chips, dealer } = tray;
        object::delete(id);
        balance::destroy_zero(chips);
        option::destroy_none(dealer);
    }

    public fun trays_prepared(ledger: &FloorLedger): u64 {
        ledger.trays_prepared
    }

    public fun trays_assigned(ledger: &FloorLedger): u64 {
        ledger.trays_assigned
    }
}
