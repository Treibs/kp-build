module coin_currency_red::mycoin {
    use sui::coin;

    public struct MYCOIN has drop {}

    fun init(witness: MYCOIN, ctx: &mut TxContext) {
        // Fabricated API: `coin::mint_new` does not exist.
        let treasury = coin::mint_new(witness, 9, b"MYC", ctx);
        transfer::public_transfer(treasury, ctx.sender());
    }
}
