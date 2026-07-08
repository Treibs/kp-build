module board::bounty {
    use std::string::String;
    use std::option;
    use sui::coin::Coin;
    use sui::sui::SUI;

    public struct Bounty has key {
        id: UID,
        task: String,
        poster: address,
        reward: Option<Coin<SUI>>,
    }

    public fun create(task: String, reward: Option<Coin<SUI>>, ctx: &mut TxContext) {
        transfer::share_object(Bounty {
            id: object::new(ctx),
            task,
            poster: ctx.sender(),
            reward,
        });
    }

    public fun defund(bounty: &mut Bounty, ctx: &TxContext): Coin<SUI> {
        assert!(bounty.poster == ctx.sender());
        option::extract(&mut bounty.reward)
    }

    public fun refund_and_close(bounty: Bounty, ctx: &TxContext) {
        assert!(bounty.poster == ctx.sender());
        let Bounty { id, task: _, poster, reward } = bounty;
        object::delete(id);
        if (option::is_some(&reward)) {
            transfer::public_transfer(option::destroy_some(reward), poster);
        } else {
            option::destroy_none(reward);
        };
    }

    public fun award(bounty: Bounty, hunter: address, ctx: &TxContext) {
        assert!(bounty.poster == ctx.sender());
        let Bounty { id, task: _, poster: _, reward } = bounty;
        object::delete(id);
        if (option::is_some(&reward)) {
            transfer::public_transfer(option::destroy_some(reward), hunter);
        } else {
            option::destroy_none(reward);
        };
    }
}
