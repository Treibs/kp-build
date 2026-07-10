module photo_booth::booth {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::TxContext;
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;

    public struct PhotoBooth has key {
        id: UID,
        next_number: u64,
        accumulated_fees: Coin<SUI>,
        fee_amount: u64,
    }

    public struct PhotoStrip has key, store {
        id: UID,
        number: u64,
    }

    fun init(ctx: &mut TxContext) {
        let booth = PhotoBooth {
            id: object::new(ctx),
            next_number: 1,
            accumulated_fees: coin::zero(ctx),
            fee_amount: 1_000_000_000,
        };
        transfer::share_object(booth);
    }

    public fun take_photo(
        booth: &mut PhotoBooth,
        payment: Coin<SUI>,
        ctx: &mut TxContext,
    ): PhotoStrip {
        assert!(coin::value(&payment) == booth.fee_amount, 0);
        
        let current = booth.next_number;
        booth.next_number = booth.next_number + 1;
        coin::join(&mut booth.accumulated_fees, payment);
        
        PhotoStrip {
            id: object::new(ctx),
            number: current,
        }
    }

    public fun sweep(booth: &mut PhotoBooth, ctx: &mut TxContext): Coin<SUI> {
        let amount = coin::value(&booth.accumulated_fees);
        coin::split(&mut booth.accumulated_fees, amount, ctx)
    }
}
