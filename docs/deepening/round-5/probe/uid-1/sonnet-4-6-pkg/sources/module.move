module gym::locker {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};
    use sui::event;
    use sui::object::ID;

    public struct FrontDeskCap has key, store {
        id: UID,
    }

    public struct Locker has key, store {
        id: UID,
        number: u64,
        combination: u64,
    }

    public struct GymPool has key {
        id: UID,
        balance: Balance<SUI>,
    }

    public struct Rekeyed has copy, drop {
        old_locker_id: ID,
        new_locker_id: ID,
        locker_number: u64,
    }

    fun init(ctx: &mut TxContext) {
        transfer::transfer(FrontDeskCap { id: object::new(ctx) }, ctx.sender());
        transfer::share_object(GymPool {
            id: object::new(ctx),
            balance: balance::zero(),
        });
    }

    public fun assign_locker(
        _cap: &FrontDeskCap,
        number: u64,
        combination: u64,
        member: address,
        ctx: &mut TxContext,
    ) {
        transfer::public_transfer(
            Locker { id: object::new(ctx), number, combination },
            member,
        );
    }

    public fun rekey(
        pool: &mut GymPool,
        old_locker: Locker,
        new_combination: u64,
        fee: Coin<SUI>,
        ctx: &mut TxContext,
    ): Locker {
        let old_locker_id = object::id(&old_locker);
        let Locker { id, number, combination: _ } = old_locker;
        object::delete(id);

        balance::join(&mut pool.balance, coin::into_balance(fee));

        let new_locker = Locker {
            id: object::new(ctx),
            number,
            combination: new_combination,
        };
        let new_locker_id = object::id(&new_locker);

        event::emit(Rekeyed { old_locker_id, new_locker_id, locker_number: number });

        new_locker
    }
}
