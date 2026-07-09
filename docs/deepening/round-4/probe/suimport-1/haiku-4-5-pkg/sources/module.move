module paywall::access {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::object;
    use sui::transfer;
    use sui::tx_context::TxContext;
    use std::string::String;

    public struct Article has key {
        id: UID,
        title: String,
        price_mist: u64,
        proceeds: Coin<SUI>,
    }

    public struct AccessPass has key, store {
        id: UID,
        article_title: String,
    }

    public struct AuthorCap has key, store {
        id: UID,
    }

    public fun create(
        title: String,
        price_mist: u64,
        ctx: &mut TxContext,
    ) {
        let article = Article {
            id: object::new(ctx),
            title,
            price_mist,
            proceeds: coin::zero(ctx),
        };
        transfer::share_object(article);

        let cap = AuthorCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, ctx.sender());
    }

    public fun unlock(
        article: &mut Article,
        payment: Coin<SUI>,
        ctx: &mut TxContext,
    ): AccessPass {
        assert!(coin::value(&payment) == article.price_mist, 0);
        coin::join(&mut article.proceeds, payment);
        
        AccessPass {
            id: object::new(ctx),
            article_title: article.title,
        }
    }

    public fun collect(
        article: &mut Article,
        _cap: &AuthorCap,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let amount = coin::value(&article.proceeds);
        coin::split(&mut article.proceeds, amount, ctx)
    }
}
