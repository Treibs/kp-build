module invoicing::contractor_invoice {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::clock::Clock;
    use sui::event;

    public struct Invoice has key, store {
        id: UID,
        contractor: address,
        client: address,
        amount: u64,
        late_fee: u64,
        due_epoch: u64,
    }

    public struct Receipt has key, store {
        id: UID,
        invoice_id: ID,
        amount_paid: u64,
    }

    public struct InvoicePaid has copy, drop {
        invoice_id: ID,
        amount_paid: u64,
    }

    public struct InvoiceVoided has copy, drop {
        invoice_id: ID,
    }

    public fun create_invoice(
        client: address,
        amount: u64,
        late_fee: u64,
        due_epoch: u64,
        ctx: &mut TxContext,
    ) {
        let invoice = Invoice {
            id: object::new(ctx),
            contractor: tx_context::sender(ctx),
            client,
            amount,
            late_fee,
            due_epoch,
        };
        transfer::share_object(invoice);
    }

    public fun amount_owed(invoice: &Invoice, clock: &Clock): u64 {
        if (clock.timestamp_ms() > invoice.due_epoch) {
            invoice.amount + invoice.late_fee
        } else {
            invoice.amount
        }
    }

    public fun pay(
        invoice: Invoice,
        payment: Coin<SUI>,
        clock: &Clock,
        ctx: &mut TxContext,
    ): Receipt {
        let payer = tx_context::sender(ctx);
        assert!(payer == invoice.client, 0);

        let invoice_id = object::uid_to_inner(&invoice.id);
        let contractor = invoice.contractor;

        let owed = amount_owed(&invoice, clock);
        let paid = coin::value(&payment);

        assert!(paid >= owed, 1);

        if (paid > owed) {
            let overpayment = paid - owed;
            let overpayment_coin = coin::split(&mut payment, overpayment, ctx);
            transfer::public_transfer(overpayment_coin, payer);
        }

        transfer::public_transfer(payment, contractor);

        let receipt = Receipt {
            id: object::new(ctx),
            invoice_id,
            amount_paid: owed,
        };

        event::emit(InvoicePaid {
            invoice_id,
            amount_paid: owed,
        });

        let Invoice { id, contractor: _, client: _, amount: _, late_fee: _, due_epoch: _ } = invoice;
        object::delete(id);

        receipt
    }

    public fun void_invoice(
        invoice: Invoice,
        ctx: &mut TxContext,
    ) {
        let caller = tx_context::sender(ctx);
        assert!(caller == invoice.contractor, 2);

        let invoice_id = object::uid_to_inner(&invoice.id);

        let Invoice { id, contractor: _, client: _, amount: _, late_fee: _, due_epoch: _ } = invoice;
        object::delete(id);

        event::emit(InvoiceVoided {
            invoice_id,
        });
    }
}
