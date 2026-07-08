module merchant_giftcard::giftcard {
    use sui::coin::{Coin, SUI};
    use sui::transfer;

    public struct GiftCard has key, store {
        id: UID,
        merchant: address,
        balance: Coin<SUI>,
    }

    public fun create_giftcard(
        merchant: address,
        balance: Coin<SUI>,
        ctx: &mut TxContext,
    ): GiftCard {
        GiftCard {
            id: object::new(ctx),
            merchant,
            balance,
        }
    }

    public fun spend(
        giftcard: &mut GiftCard,
        amount: u64,
        ctx: &mut TxContext,
    ) {
        let payment = coin::split(&mut giftcard.balance, amount, ctx);
        transfer::public_transfer(payment, giftcard.merchant);
    }

    public fun topup(
        giftcard: &mut GiftCard,
        additional: Coin<SUI>,
    ) {
        coin::join(&mut giftcard.balance, additional);
    }

    public fun cashout(
        giftcard: GiftCard,
        ctx: &TxContext,
    ) {
        let GiftCard { id, merchant: _, balance } = giftcard;
        object::delete(id);
        transfer::public_transfer(balance, ctx.sender());
    }

    public fun merchant(giftcard: &GiftCard): address {
        giftcard.merchant
    }

    public fun balance(giftcard: &GiftCard): u64 {
        coin::value(&giftcard.balance)
    }
}
