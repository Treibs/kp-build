module shop::consign {
    use std::option::{Self, Option};
    use sui::coin::Coin;
    use sui::sui::SUI;

    public struct Shop<T: store> has key {
        id: UID,
        shopkeeper: address,
        item: Option<T>,
        price: u64,
    }

    public fun create(shopkeeper: address, ctx: &mut TxContext): Shop<T> {
        Shop {
            id: object::new(ctx),
            shopkeeper,
            item: option::none(),
            price: 0,
        }
    }

    public fun stock<T: store>(
        shop: &mut Shop<T>,
        item: T,
        price: u64,
    ) {
        if (option::is_some(&shop.item)) {
            let old = option::extract(&mut shop.item);
            transfer::public_transfer(old, shop.shopkeeper);
        };
        option::fill(&mut shop.item, item);
        shop.price = price;
    }

    public fun buy<T: store>(
        shop: &mut Shop<T>,
        payment: Coin<SUI>,
        _ctx: &mut TxContext,
    ): T {
        assert!(option::is_some(&shop.item), 0);
        assert!(payment.value() == shop.price, 1);
        
        transfer::public_transfer(payment, shop.shopkeeper);
        option::extract(&mut shop.item)
    }
}
