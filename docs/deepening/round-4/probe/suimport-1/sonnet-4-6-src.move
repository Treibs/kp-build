module paywall::access {
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};
    use sui::sui::SUI;
    use sui::object::ID;
    use std::string::String;

    public struct Article has key {
        id: UID,
        title: String,
        price: u64,
        proceeds: Balance<SUI>,
    }

    public struct AuthorCap has key, store {
        id: UID,
        article_id: ID,
    }

    public struct AccessPass has key, store {
        id: UID,
        title: String,
    }

    public fun create(title: String, price: u64, ctx: &mut TxContext): AuthorCap {
        let article = Article {
            id: object::new(ctx),
            title,
            price,
            proceeds: balance::zero(),
        };
        let article_id = object::id(&article);
        transfer::share_object(article);
        AuthorCap {
            id: object::new(ctx),
            article_id,
        }
    }

    public fun unlock(
        article: &mut Article,
        payment: Coin<SUI>,
        ctx: &mut TxContext,
    ): AccessPass {
        assert!(coin::value(&payment) == article.price);
        balance::join(&mut article.proceeds, coin::into_balance(payment));
        AccessPass {
            id: object::new(ctx),
            title: article.title,
        }
    }

    public fun collect(
        cap: &AuthorCap,
        article: &mut Article,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        assert!(cap.article_id == object::id(article));
        let amount = balance::value(&article.proceeds);
        coin::from_balance(balance::split(&mut article.proceeds, amount), ctx)
    }
}
