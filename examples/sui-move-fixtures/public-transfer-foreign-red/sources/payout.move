module public_transfer_foreign_red::payout {
    use sui::coin::Coin;
    use sui::sui::SUI;

    // `transfer::transfer` is the PRIVATE transfer: callable only inside
    // the module that defines the object type. `Coin` lives in
    // `sui::coin`, so this call is rejected here.
    public fun pay(coin: Coin<SUI>, recipient: address) {
        transfer::transfer(coin, recipient);
    }
}
