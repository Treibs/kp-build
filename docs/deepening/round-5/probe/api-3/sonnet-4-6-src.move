module family_budget::envelopes {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;

    public fun distribute(
        mut budget: Coin<SUI>,
        labels: vector<vector<u8>>,
        recipients: vector<address>,
        amounts: vector<u64>,
        ctx: &mut TxContext
    ): Coin<SUI> {
        let n = vector::length(&labels);
        assert!(vector::length(&recipients) == n);
        assert!(vector::length(&amounts) == n);

        // abort before any transfer if envelopes exceed budget
        let mut total = 0u64;
        let mut i = 0u64;
        while (i < n) {
            total = total + *vector::borrow(&amounts, i);
            i = i + 1;
        };
        assert!(coin::value(&budget) >= total);

        let mut j = 0u64;
        while (j < n) {
            let amount = *vector::borrow(&amounts, j);
            let recipient = *vector::borrow(&recipients, j);
            transfer::public_transfer(coin::split(&mut budget, amount, ctx), recipient);
            j = j + 1;
        };

        budget
    }
}
