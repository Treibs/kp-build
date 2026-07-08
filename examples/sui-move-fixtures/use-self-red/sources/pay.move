module use_self_red::pay {
    // Rust-style lowercase `self` is not the Move keyword: group imports
    // must use capital `Self` to bind the module itself.
    use sui::coin::{self, Coin};
    use sui::sui::SUI;

    public fun amount(payment: &Coin<SUI>): u64 {
        coin::value(payment)
    }
}
