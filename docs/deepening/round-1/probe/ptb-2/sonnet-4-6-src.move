module merge::merger {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;

    const EEmptyVector: u64 = 0;

    public fun merge_and_transfer(mut coins: vector<Coin<SUI>>, recipient: address, ctx: &mut TxContext) {
        assert!(!coins.is_empty(), EEmptyVector);
        let mut merged = coins.pop_back();
        while (!coins.is_empty()) {
            let c = coins.pop_back();
            merged.join(c);
        };
        coins.destroy_empty();
        transfer::public_transfer(merged, recipient);
    }
}
