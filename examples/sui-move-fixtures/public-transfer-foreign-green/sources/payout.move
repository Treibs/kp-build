module public_transfer_foreign_green::payout {
    use sui::coin::Coin;
    use sui::sui::SUI;

    // `Coin` is defined in `sui::coin` (a foreign module from here) and
    // has `store`, so the public transfer function is the right call.
    public fun pay(coin: Coin<SUI>, recipient: address) {
        transfer::public_transfer(coin, recipient);
    }
}
