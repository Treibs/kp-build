module 0x0::envelope_budget {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::transfer;
    use sui::tx_context::TxContext;

    public struct Envelope has copy, drop {
        label: vector<u8>,
        amount: u64,
        recipient: address,
    }

    public fun split_budget(
        mut budget: Coin<SUI>,
        envelopes: vector<Envelope>,
        ctx: &mut TxContext,
    ) {
        let mut total = 0u64;
        let mut i = 0;
        
        while (i < vector::length(&envelopes)) {
            total = total + vector::borrow(&envelopes, i).amount;
            i = i + 1;
        };
        
        assert!(total <= coin::value(&budget), 0);

        i = 0;
        while (i < vector::length(&envelopes)) {
            let env = vector::borrow(&envelopes, i);
            let coin_out = coin::split(&mut budget, env.amount, ctx);
            transfer::public_transfer(coin_out, env.recipient);
            i = i + 1;
        };

        transfer::public_transfer(budget, ctx.sender());
    }
}
