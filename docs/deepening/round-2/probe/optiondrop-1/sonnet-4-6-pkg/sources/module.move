module shop::consign {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;

    public struct Shop<T: key + store> has key {
        id: UID,
        shopkeeper: address,
        item: std::option::Option<T>,
        price: u64,
    }

    public fun create<T: key + store>(ctx: &mut TxContext) {
        transfer::transfer(
            Shop<T> {
                id: object::new(ctx),
                shopkeeper: ctx.sender(),
                item: std::option::none(),
                price: 0,
            },
            ctx.sender(),
        );
    }

    public fun stock<T: key + store>(shop: &mut Shop<T>, item: T, price: u64) {
        if (shop.item.is_some()) {
            let old_item = shop.item.extract();
            transfer::public_transfer(old_item, shop.shopkeeper);
        };
        shop.item.fill(item);
        shop.price = price;
    }

    public fun buy<T: key + store>(shop: &mut Shop<T>, payment: Coin<SUI>, ctx: &mut TxContext) {
        assert!(shop.item.is_some());
        assert!(payment.value() == shop.price);
        let item = shop.item.extract();
        transfer::public_transfer(payment, shop.shopkeeper);
        transfer::public_transfer(item, ctx.sender());
    }
}
