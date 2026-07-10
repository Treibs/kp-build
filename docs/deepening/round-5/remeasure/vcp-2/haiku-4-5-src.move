module parking_garage::garage {
    use sui::object::{Self, UID};
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};
    use sui::sui::SUI;
    use sui::clock::Clock;
    use sui::tx_context::TxContext;

    public struct GarageTicket has key, store {
        id: UID,
        entry_epoch: u64,
        validated: bool,
    }

    public struct ValidatorCap has key, store {
        id: UID,
    }

    public struct OperatorCap has key, store {
        id: UID,
    }

    public struct FeePool has key {
        id: UID,
        fees: Balance<SUI>,
    }

    public fun entry(
        clock: &Clock,
        ctx: &mut TxContext,
    ): GarageTicket {
        GarageTicket {
            id: object::new(ctx),
            entry_epoch: clock.timestamp_ms(),
            validated: false,
        }
    }

    public fun validate(
        ticket: &mut GarageTicket,
        _cap: &ValidatorCap,
    ) {
        ticket.validated = true;
    }

    public fun exit(
        ticket: GarageTicket,
        payment: Coin<SUI>,
        clock: &Clock,
        fee_pool: &mut FeePool,
        hourly_rate: u64,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let GarageTicket { id, entry_epoch, validated } = ticket;
        object::delete(id);

        if (validated) {
            payment
        } else {
            let current_epoch = clock.timestamp_ms();
            let epochs_elapsed = current_epoch - entry_epoch;
            let fee_amount = epochs_elapsed * hourly_rate;
            let payment_value = coin::value(&payment);

            if (fee_amount >= payment_value) {
                let balance = coin::into_balance(payment);
                balance::join(&mut fee_pool.fees, balance);
                coin::zero(ctx)
            } else {
                let (fee_coin, change_coin) = coin::split(payment, fee_amount, ctx);
                let fee_balance = coin::into_balance(fee_coin);
                balance::join(&mut fee_pool.fees, fee_balance);
                change_coin
            }
        }
    }

    public fun sweep_fees(
        fee_pool: &mut FeePool,
        _cap: &OperatorCap,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let fees = balance::withdraw_all(&mut fee_pool.fees);
        coin::from_balance(fees, ctx)
    }

    public fun create_fee_pool(ctx: &mut TxContext): FeePool {
        FeePool {
            id: object::new(ctx),
            fees: balance::zero(),
        }
    }

    public fun create_validator_cap(ctx: &mut TxContext): ValidatorCap {
        ValidatorCap {
            id: object::new(ctx),
        }
    }

    public fun create_operator_cap(ctx: &mut TxContext): OperatorCap {
        OperatorCap {
            id: object::new(ctx),
        }
    }
}
