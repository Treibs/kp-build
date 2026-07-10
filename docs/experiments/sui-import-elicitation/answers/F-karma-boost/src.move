module 0x0::pay_to_boost {
    use sui::coin::{Coin, split};
    use sui::balance::Balance;
    use sui::sui::SUI;
    use sui::event;

    public struct Post has key, store {
        id: UID,
        author: address,
        boost_count: u64,
        collected_sui: Balance<SUI>,
    }

    public struct BoostAdded has copy, drop {
        post_id: ID,
        new_total: u64,
    }

    public struct SuiWithdrawn has copy, drop {
        post_id: ID,
        amount: u64,
    }

    const BOOST_FEE: u64 = 1_000_000_000;

    public fun create_post(ctx: &mut TxContext): Post {
        Post {
            id: object::new(ctx),
            author: ctx.sender(),
            boost_count: 0,
            collected_sui: sui::balance::zero<SUI>(),
        }
    }

    public fun boost_post(
        post: &mut Post,
        payment: &mut Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        assert!(payment.value() >= BOOST_FEE, 0);
        let fee_coin = split(payment, BOOST_FEE, ctx);
        sui::balance::join(&mut post.collected_sui, sui::coin::into_balance(fee_coin));
        post.boost_count = post.boost_count + 1;
        event::emit(BoostAdded {
            post_id: object::id(post),
            new_total: post.boost_count,
        });
    }

    public fun withdraw_boosts(
        post: &mut Post,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        assert!(ctx.sender() == post.author, 1);
        let amount = sui::balance::value(&post.collected_sui);
        let balance = sui::balance::withdraw_all(&mut post.collected_sui);
        event::emit(SuiWithdrawn {
            post_id: object::id(post),
            amount,
        });
        sui::coin::from_balance(balance, ctx)
    }
}
