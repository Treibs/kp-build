module layaway::plan {
    use sui::balance::{Self, Balance};
    use sui::clock::Clock;
    use sui::coin::{Self, Coin};
    use sui::event;
    use sui::sui::SUI;

    const ENotBuyer: u64 = 1;
    const ENotSeller: u64 = 2;
    const EDeadlineNotPassed: u64 = 3;
    const EInsufficientPayment: u64 = 4;

    public struct LayawayPlan<T: key + store> has key, store {
        id: UID,
        seller: address,
        buyer: address,
        item: T,
        total_price: u64,
        cancellation_fee: u64,
        deadline_interval: u64,
        last_payment_time: u64,
        accumulated_balance: Balance<SUI>,
    }

    public struct PlanCreated has copy, drop {
        plan_id: ID,
        seller: address,
        buyer: address,
        total_price: u64,
    }

    public struct PaymentMade has copy, drop {
        plan_id: ID,
        amount: u64,
        accumulated: u64,
    }

    public struct PlanCompleted has copy, drop {
        plan_id: ID,
        accumulated: u64,
    }

    public struct PlanCancelledByBuyer has copy, drop {
        plan_id: ID,
    }

    public struct PlanCancelledBySeller has copy, drop {
        plan_id: ID,
    }

    public fun create_plan<T: key + store>(
        item: T,
        seller: address,
        buyer: address,
        total_price: u64,
        cancellation_fee: u64,
        deadline_interval: u64,
        clock: &Clock,
        ctx: &mut TxContext,
    ) {
        let plan = LayawayPlan {
            id: object::new(ctx),
            seller,
            buyer,
            item,
            total_price,
            cancellation_fee,
            deadline_interval,
            last_payment_time: clock.timestamp_ms(),
            accumulated_balance: balance::zero(),
        };

        event::emit(PlanCreated {
            plan_id: object::id(&plan),
            seller,
            buyer,
            total_price,
        });

        transfer::share_object(plan);
    }

    public fun make_payment<T: key + store>(
        plan: &mut LayawayPlan<T>,
        payment: Coin<SUI>,
        clock: &Clock,
        ctx: &mut TxContext,
    ) {
        assert!(ctx.sender() == plan.buyer, ENotBuyer);

        let amount = coin::value(&payment);
        plan.accumulated_balance.join(coin::into_balance(payment));
        plan.last_payment_time = clock.timestamp_ms();

        event::emit(PaymentMade {
            plan_id: object::id(plan),
            amount,
            accumulated: balance::value(&plan.accumulated_balance),
        });
    }

    public fun complete_purchase<T: key + store>(
        plan: LayawayPlan<T>,
        ctx: &mut TxContext,
    ) {
        let plan_id = object::id(&plan);

        let LayawayPlan {
            id,
            seller,
            buyer,
            item,
            total_price,
            cancellation_fee: _,
            deadline_interval: _,
            last_payment_time: _,
            mut accumulated_balance,
        } = plan;

        let accumulated = balance::value(&accumulated_balance);
        assert!(accumulated >= total_price, EInsufficientPayment);

        let seller_payment = balance::split(&mut accumulated_balance, total_price);
        transfer::public_transfer(coin::from_balance(seller_payment, ctx), seller);

        if (balance::value(&accumulated_balance) > 0) {
            transfer::public_transfer(coin::from_balance(accumulated_balance, ctx), buyer);
        } else {
            balance::destroy_zero(accumulated_balance);
        };

        transfer::public_transfer(item, buyer);

        event::emit(PlanCompleted { plan_id, accumulated });
        object::delete(id);
    }

    public fun cancel_by_buyer<T: key + store>(
        plan: LayawayPlan<T>,
        ctx: &mut TxContext,
    ) {
        let plan_id = object::id(&plan);

        let LayawayPlan {
            id,
            seller,
            buyer,
            item,
            total_price: _,
            cancellation_fee,
            deadline_interval: _,
            last_payment_time: _,
            mut accumulated_balance,
        } = plan;

        assert!(ctx.sender() == buyer, ENotBuyer);

        let accumulated = balance::value(&accumulated_balance);
        let fee_amount = if (accumulated >= cancellation_fee) {
            cancellation_fee
        } else {
            accumulated
        };

        if (fee_amount > 0) {
            let fee = balance::split(&mut accumulated_balance, fee_amount);
            transfer::public_transfer(coin::from_balance(fee, ctx), seller);
        };

        if (balance::value(&accumulated_balance) > 0) {
            transfer::public_transfer(coin::from_balance(accumulated_balance, ctx), buyer);
        } else {
            balance::destroy_zero(accumulated_balance);
        };

        transfer::public_transfer(item, seller);

        event::emit(PlanCancelledByBuyer { plan_id });
        object::delete(id);
    }

    public fun cancel_by_seller<T: key + store>(
        plan: LayawayPlan<T>,
        clock: &Clock,
        ctx: &mut TxContext,
    ) {
        let plan_id = object::id(&plan);

        let LayawayPlan {
            id,
            seller,
            buyer,
            item,
            total_price: _,
            cancellation_fee,
            deadline_interval,
            last_payment_time,
            mut accumulated_balance,
        } = plan;

        assert!(ctx.sender() == seller, ENotSeller);

        let current_time = clock.timestamp_ms();
        assert!(current_time - last_payment_time > deadline_interval, EDeadlineNotPassed);

        let accumulated = balance::value(&accumulated_balance);
        let fee_amount = if (accumulated >= cancellation_fee) {
            cancellation_fee
        } else {
            accumulated
        };

        if (fee_amount > 0) {
            let fee = balance::split(&mut accumulated_balance, fee_amount);
            transfer::public_transfer(coin::from_balance(fee, ctx), seller);
        };

        if (balance::value(&accumulated_balance) > 0) {
            transfer::public_transfer(coin::from_balance(accumulated_balance, ctx), buyer);
        } else {
            balance::destroy_zero(accumulated_balance);
        };

        transfer::public_transfer(item, seller);

        event::emit(PlanCancelledBySeller { plan_id });
        object::delete(id);
    }

    public fun remaining_owed<T: key + store>(plan: &LayawayPlan<T>): u64 {
        let accumulated = balance::value(&plan.accumulated_balance);
        if (accumulated >= plan.total_price) {
            0
        } else {
            plan.total_price - accumulated
        }
    }
}
