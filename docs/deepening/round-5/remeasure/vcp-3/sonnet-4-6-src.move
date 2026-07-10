module barbershop::shop {
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};
    use sui::sui::SUI;

    public struct BarberShop has key {
        id: UID,
        pool: Balance<SUI>,
        barber_in: bool,
        status_epoch: u64,
    }

    public struct BarberCap has key, store {
        id: UID,
    }

    public struct OwnerCap has key, store {
        id: UID,
    }

    public struct CustomerCard has key, store {
        id: UID,
        visit_count: u64,
    }

    fun init(ctx: &mut TxContext) {
        transfer::share_object(BarberShop {
            id: object::new(ctx),
            pool: balance::zero(),
            barber_in: false,
            status_epoch: 0,
        });
        transfer::transfer(BarberCap { id: object::new(ctx) }, ctx.sender());
        transfer::transfer(OwnerCap { id: object::new(ctx) }, ctx.sender());
    }

    public fun mark_in(_cap: &BarberCap, shop: &mut BarberShop, ctx: &TxContext) {
        shop.barber_in = true;
        shop.status_epoch = ctx.epoch();
    }

    public fun mark_out(_cap: &BarberCap, shop: &mut BarberShop, ctx: &TxContext) {
        shop.barber_in = false;
        shop.status_epoch = ctx.epoch();
    }

    public fun new_card(ctx: &mut TxContext): CustomerCard {
        CustomerCard { id: object::new(ctx), visit_count: 0 }
    }

    public fun walk_in(
        shop: &mut BarberShop,
        card: &mut CustomerCard,
        payment: Coin<SUI>,
        ctx: &TxContext,
    ) {
        if (shop.barber_in && shop.status_epoch == ctx.epoch()) {
            coin::put(&mut shop.pool, payment);
            card.visit_count = card.visit_count + 1;
        } else {
            transfer::public_transfer(payment, ctx.sender());
        };
    }

    public fun sweep(_cap: &OwnerCap, shop: &mut BarberShop, ctx: &mut TxContext) {
        let amount = balance::value(&shop.pool);
        assert!(amount > 0);
        let payout = coin::take(&mut shop.pool, amount, ctx);
        transfer::public_transfer(payout, ctx.sender());
    }

    public fun visit_count(card: &CustomerCard): u64 {
        card.visit_count
    }

    public fun barber_is_in(shop: &BarberShop, ctx: &TxContext): bool {
        shop.barber_in && shop.status_epoch == ctx.epoch()
    }
}
