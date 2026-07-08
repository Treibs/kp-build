module subscription::registry {
    use sui::object::{Self, UID};
    use sui::tx_context::{Self, TxContext};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};
    use sui::vec_map::{Self, VecMap};

    public struct SubscriptionRegistry has key {
        id: UID,
        operator: address,
        price_per_period: u64,
        period_length_epochs: u64,
        fees: Balance<SUI>,
        subscribers: VecMap<address, u64>,
    }

    public fun create(
        price_per_period: u64,
        period_length_epochs: u64,
        ctx: &mut TxContext,
    ): SubscriptionRegistry {
        SubscriptionRegistry {
            id: object::new(ctx),
            operator: tx_context::sender(ctx),
            price_per_period,
            period_length_epochs,
            fees: balance::zero(),
            subscribers: vec_map::empty(),
        }
    }

    public fun subscribe(
        registry: &mut SubscriptionRegistry,
        payment: Coin<SUI>,
        periods: u64,
        ctx: &mut TxContext,
    ) {
        let amount = coin::value(&payment);
        let required = registry.price_per_period * periods;
        assert!(amount >= required, 0);
        
        let subscriber = tx_context::sender(ctx);
        let current_epoch = tx_context::epoch(ctx);
        let extension = registry.period_length_epochs * periods;
        
        if (vec_map::contains(&registry.subscribers, &subscriber)) {
            let paid_through = vec_map::get_mut(&mut registry.subscribers, &subscriber);
            let start_epoch = if (*paid_through > current_epoch) {
                *paid_through
            } else {
                current_epoch
            };
            *paid_through = start_epoch + extension;
        } else {
            vec_map::insert(&mut registry.subscribers, subscriber, current_epoch + extension);
        };
        
        balance::join(&mut registry.fees, coin::into_balance(payment));
    }

    public fun is_active(
        registry: &SubscriptionRegistry,
        subscriber: address,
        ctx: &TxContext,
    ): bool {
        let current_epoch = tx_context::epoch(ctx);
        if (vec_map::contains(&registry.subscribers, &subscriber)) {
            let paid_through = vec_map::get(&registry.subscribers, &subscriber);
            *paid_through > current_epoch
        } else {
            false
        }
    }

    public fun withdraw(
        registry: &mut SubscriptionRegistry,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        assert!(tx_context::sender(ctx) == registry.operator, 1);
        
        let fees = balance::withdraw_all(&mut registry.fees);
        coin::from_balance(fees, ctx)
    }
}
