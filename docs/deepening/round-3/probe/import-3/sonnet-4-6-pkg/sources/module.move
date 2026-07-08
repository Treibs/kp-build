module match::donation {
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};
    use sui::sui::SUI;

    public struct SponsorCap has key, store {
        id: UID,
    }

    public struct MatchPool has key {
        id: UID,
        reserves: Balance<SUI>,
        charity: address,
    }

    public fun create(funding: Coin<SUI>, charity: address, ctx: &mut TxContext): SponsorCap {
        let pool = MatchPool {
            id: object::new(ctx),
            reserves: coin::into_balance(funding),
            charity,
        };
        transfer::share_object(pool);
        SponsorCap { id: object::new(ctx) }
    }

    public fun donate(pool: &mut MatchPool, gift: Coin<SUI>, ctx: &mut TxContext) {
        let gift_value = coin::value(&gift);
        let reserve_value = balance::value(&pool.reserves);
        let match_amount = if (reserve_value >= gift_value) {
            gift_value
        } else {
            reserve_value
        };
        let mut combined = gift;
        if (match_amount > 0) {
            let matched = coin::from_balance(balance::split(&mut pool.reserves, match_amount), ctx);
            coin::join(&mut combined, matched);
        };
        transfer::public_transfer(combined, pool.charity);
    }

    public fun reserves(pool: &MatchPool): u64 {
        balance::value(&pool.reserves)
    }

    public fun refill(_cap: &SponsorCap, pool: &mut MatchPool, funding: Coin<SUI>) {
        balance::join(&mut pool.reserves, coin::into_balance(funding));
    }
}
