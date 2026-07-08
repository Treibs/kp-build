module use_self_green::pay {
    // Group imports name the module itself with the capital `Self` keyword.
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;

    public fun amount(payment: &Coin<SUI>): u64 {
        coin::value(payment)
    }
}
