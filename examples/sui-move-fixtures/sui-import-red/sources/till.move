module sui_import_red::till {
    // SUI does not live in sui::coin — importing it from there is the
    // wrong-module shape the held-out record keeps producing. It is
    // declared in sui::sui (see the green fixture).
    use sui::coin::{Self, Coin, SUI};
    use sui::balance::{Self, Balance};

    public struct Till has key {
        id: UID,
        takings: Balance<SUI>,
    }

    public fun open(ctx: &mut TxContext): Till {
        Till { id: object::new(ctx), takings: balance::zero() }
    }

    public fun ring_up(till: &mut Till, payment: Coin<SUI>) {
        coin::put(&mut till.takings, payment);
    }
}
