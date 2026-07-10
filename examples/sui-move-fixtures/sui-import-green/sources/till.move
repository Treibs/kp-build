module sui_import_green::till {
    // The SUI coin type is declared in the `sui::sui` module; it is used
    // *through* Coin/Balance everywhere, but imported from sui::sui.
    use sui::sui::SUI;
    use sui::coin::{Self, Coin};
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

    public fun takings(till: &Till): u64 {
        balance::value(&till.takings)
    }
}
