module ev_charging::station {
    use sui::object::{Self, UID};
    use sui::tx_context::{Self, TxContext};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};
    use sui::transfer;

    public struct Station has key {
        id: UID,
        operator: address,
        proceeds: Balance<SUI>,
        cost_per_epoch: u64,
    }

    public struct ChargeSession has key {
        id: UID,
        driver: address,
        escrow: Coin<SUI>,
        start_epoch: u64,
        cost_per_epoch: u64,
    }

    public fun create_station(cost_per_epoch: u64, ctx: &mut TxContext) {
        transfer::share_object(Station {
            id: object::new(ctx),
            operator: tx_context::sender(ctx),
            proceeds: balance::zero(),
            cost_per_epoch,
        });
    }

    public fun plug_in(
        station: &Station,
        escrow: Coin<SUI>,
        ctx: &mut TxContext,
    ): ChargeSession {
        ChargeSession {
            id: object::new(ctx),
            driver: tx_context::sender(ctx),
            escrow,
            start_epoch: tx_context::epoch(ctx),
            cost_per_epoch: station.cost_per_epoch,
        }
    }

    public fun unplug(
        station: &mut Station,
        session: ChargeSession,
        ctx: &mut TxContext,
    ) {
        let ChargeSession {
            id,
            driver,
            escrow,
            start_epoch,
            cost_per_epoch,
        } = session;

        let mut escrow = escrow;
        object::delete(id);

        let end_epoch = tx_context::epoch(ctx);
        let epochs_used = end_epoch - start_epoch;
        let cost = epochs_used * cost_per_epoch;
        let escrow_amount = coin::value(&escrow);

        if (cost >= escrow_amount) {
            balance::join(&mut station.proceeds, coin::into_balance(escrow));
        } else {
            let charge_coin = coin::split(&mut escrow, cost, ctx);
            balance::join(&mut station.proceeds, coin::into_balance(charge_coin));
            transfer::public_transfer(escrow, driver);
        };
    }

    public fun withdraw_proceeds(
        station: &mut Station,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        assert!(tx_context::sender(ctx) == station.operator, 0);
        let amount = balance::value(&station.proceeds);
        coin::from_balance(balance::split(&mut station.proceeds, amount), ctx)
    }
}
