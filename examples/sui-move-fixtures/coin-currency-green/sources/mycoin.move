module coin_currency_green::mycoin {
    use sui::coin;

    public struct MYCOIN has drop {}

    fun init(witness: MYCOIN, ctx: &mut TxContext) {
        let (treasury, metadata) = coin::create_currency(
            witness,
            9,
            b"MYC",
            b"My Coin",
            b"Example coin",
            option::none(),
            ctx,
        );
        transfer::public_freeze_object(metadata);
        transfer::public_transfer(treasury, ctx.sender());
    }
}
