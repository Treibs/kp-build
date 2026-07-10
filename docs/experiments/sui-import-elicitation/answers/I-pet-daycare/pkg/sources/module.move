module daycare::pet_daycare {
    use sui::object::{Self, UID, ID};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::transfer;
    use sui::tx_context::TxContext;
    use sui::dynamic_field;

    public struct Pet has key, store {
        id: UID,
    }

    public struct Daycare has key {
        id: UID,
        balance: Coin<SUI>,
        operator: address,
    }

    public struct CheckedInPet has store {
        pet: Pet,
        owner: address,
        epoch: u64,
    }

    public fun create_daycare(operator: address, ctx: &mut TxContext) {
        let daycare = Daycare {
            id: object::new(ctx),
            balance: coin::zero(ctx),
            operator,
        };
        transfer::share_object(daycare);
    }

    public fun check_in(
        daycare: &mut Daycare,
        pet: Pet,
        ctx: &mut TxContext,
    ) {
        let pet_id = object::id(&pet);
        dynamic_field::add(
            &mut daycare.id,
            pet_id,
            CheckedInPet {
                pet,
                owner: ctx.sender(),
                epoch: ctx.epoch(),
            },
        );
    }

    public fun check_out(
        daycare: &mut Daycare,
        pet_id: ID,
        mut payment: Coin<SUI>,
        ctx: &mut TxContext,
    ): Pet {
        let checked_in: CheckedInPet = dynamic_field::remove(&mut daycare.id, pet_id);

        assert!(ctx.sender() == checked_in.owner);

        let epochs_elapsed = ctx.epoch() - checked_in.epoch;
        let cost = epochs_elapsed * 1000000000;
        assert!(coin::value(&payment) >= cost);

        let payment_amount = coin::split(&mut payment, cost, ctx);
        coin::join(&mut daycare.balance, payment_amount);
        
        if (coin::value(&payment) > 0) {
            transfer::public_transfer(payment, ctx.sender());
        } else {
            coin::destroy_zero(payment);
        };

        checked_in.pet
    }

    public fun withdraw(daycare: &mut Daycare, ctx: &mut TxContext): Coin<SUI> {
        assert!(ctx.sender() == daycare.operator);
        
        let amount = coin::value(&daycare.balance);
        coin::split(&mut daycare.balance, amount, ctx)
    }
}
