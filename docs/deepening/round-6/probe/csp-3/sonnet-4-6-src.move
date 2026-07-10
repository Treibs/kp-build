module returns_counter::counter {
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};
    use sui::sui::SUI;
    use sui::table::{Self, Table};
    use sui::event;

    public struct Receipt has key, store {
        id: UID,
        price_paid: u64,
    }

    public struct ReturnCounter has key {
        id: UID,
        float_balance: Balance<SUI>,
        processed_receipts: Table<ID, Receipt>,
        refunds_processed: u64,
    }

    public struct RestockEvent has copy, drop {
        receipt_id: ID,
        price_paid: u64,
        refund_amount: u64,
    }

    fun init(ctx: &mut TxContext) {
        transfer::share_object(ReturnCounter {
            id: object::new(ctx),
            float_balance: balance::zero(),
            processed_receipts: table::new(ctx),
            refunds_processed: 0,
        });
    }

    public fun issue_receipt(price_paid: u64, ctx: &mut TxContext): Receipt {
        Receipt {
            id: object::new(ctx),
            price_paid,
        }
    }

    public fun fund_float(counter: &mut ReturnCounter, payment: Coin<SUI>) {
        balance::join(&mut counter.float_balance, coin::into_balance(payment));
    }

    public fun process_return(
        counter: &mut ReturnCounter,
        receipt: Receipt,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let price_paid = receipt.price_paid;
        let refund_amount = price_paid * 80 / 100;
        let receipt_id = object::id(&receipt);

        event::emit(RestockEvent {
            receipt_id,
            price_paid,
            refund_amount,
        });

        table::add(&mut counter.processed_receipts, receipt_id, receipt);
        counter.refunds_processed = counter.refunds_processed + 1;

        coin::from_balance(
            balance::split(&mut counter.float_balance, refund_amount),
            ctx,
        )
    }

    public fun refunds_processed(counter: &ReturnCounter): u64 {
        counter.refunds_processed
    }

    public fun float_balance(counter: &ReturnCounter): u64 {
        balance::value(&counter.float_balance)
    }
}
