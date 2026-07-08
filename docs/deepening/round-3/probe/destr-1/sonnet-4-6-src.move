module party::pinata {
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;

    public struct Toy has key, store {
        id: UID,
    }

    public struct Pinata has key {
        id: UID,
        candy: Balance<SUI>,
        toy: Toy,
    }

    public fun fill(payment: Coin<SUI>, ctx: &mut TxContext): Pinata {
        let toy = Toy { id: object::new(ctx) };
        Pinata {
            id: object::new(ctx),
            candy: coin::into_balance(payment),
            toy,
        }
    }

    public fun smash(pinata: Pinata, ctx: &mut TxContext) {
        let smasher = ctx.sender();
        let Pinata { id, candy, toy } = pinata;
        object::delete(id);
        transfer::public_transfer(coin::from_balance(candy, ctx), smasher);
        transfer::public_transfer(toy, smasher);
    }
}
