module merchant::giftcard {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;

    public struct GiftCard has key, store {
        id: UID,
        merchant: address,
        balance: Balance<SUI>,
    }

    public fun create(
        merchant: address,
        amount: Coin<SUI>,
        ctx: &mut TxContext,
    ): GiftCard {
        GiftCard {
            id: object::new(ctx),
            merchant,
            balance: coin::into_balance(amount),
        }
    }

    public fun spend(
        card: &mut GiftCard,
        amount: u64,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        assert!(tx_context::sender(ctx) == card.merchant, EWrongMerchant);
        let withdrawn = balance::split(&mut card.balance, amount);
        coin::from_balance(withdrawn, ctx)
    }

    public fun topup(
        card: &mut GiftCard,
        amount: Coin<SUI>,
    ) {
        balance::join(&mut card.balance, coin::into_balance(amount));
    }

    public fun cashout(
        card: GiftCard,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let GiftCard { id, balance, merchant: _ } = card;
        object::delete(id);
        coin::from_balance(balance, ctx)
    }

    public fun get_balance(card: &GiftCard): u64 {
        balance::value(&card.balance)
    }

    public fun get_merchant(card: &GiftCard): address {
        card.merchant
    }

    const EWrongMerchant: u64 = 0;
}
