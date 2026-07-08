module board::bounty {
    use std::string::String;
    use sui::coin::Coin;
    use sui::sui::SUI;
    use std::option::{Self, Option};

    public struct Bounty has key {
        id: UID,
        task: String,
        reward: Option<Coin<SUI>>,
    }

    public fun create(task: String, reward: Option<Coin<SUI>>, ctx: &mut TxContext) {
        let bounty = Bounty {
            id: object::new(ctx),
            task,
            reward,
        };
        transfer::share_object(bounty);
    }

    public fun defund(bounty: &mut Bounty): Option<Coin<SUI>> {
        if (option::is_some(&bounty.reward)) {
            option::some(option::extract(&mut bounty.reward))
        } else {
            option::none()
        }
    }

    public fun refund_and_close(bounty: Bounty): Option<Coin<SUI>> {
        let Bounty { id, task: _, reward } = bounty;
        object::delete(id);
        reward
    }

    public fun award(bounty: Bounty, hunter: address) {
        let Bounty { id, task: _, reward } = bounty;
        if (option::is_some(&reward)) {
            let coin = option::destroy_some(reward);
            transfer::public_transfer(coin, hunter);
        } else {
            option::destroy_none(reward);
        };
        object::delete(id);
    }
}
