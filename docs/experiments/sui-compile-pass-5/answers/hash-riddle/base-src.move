module riddle_bounty::riddle {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::coin::Coin;
    use sui::sui::SUI;
    use sui::hash;

    struct Riddle has key {
        id: UID,
        poser: address,
        answer_hash: vector<u8>,
        prize: Coin<SUI>,
        created_epoch: u64,
        max_epochs: u64,
    }

    public fun create_riddle(
        answer_hash: vector<u8>,
        prize: Coin<SUI>,
        max_epochs: u64,
        ctx: &mut TxContext,
    ) {
        assert!(vector::length(&answer_hash) == 32, 0);
        
        let riddle = Riddle {
            id: object::new(ctx),
            poser: tx_context::sender(ctx),
            answer_hash,
            prize,
            created_epoch: tx_context::epoch(ctx),
            max_epochs,
        };
        
        transfer::share_object(riddle);
    }

    public fun solve(
        riddle: Riddle,
        answer: vector<u8>,
        ctx: &mut TxContext,
    ) {
        let answer_hash = hash::sha3_256(&answer);
        assert!(answer_hash == riddle.answer_hash, 1);
        
        let Riddle {
            id,
            poser: _,
            answer_hash: _,
            prize,
            created_epoch: _,
            max_epochs: _,
        } = riddle;
        
        object::delete(id);
        transfer::public_transfer(prize, tx_context::sender(ctx));
    }

    public fun reclaim(
        riddle: Riddle,
        ctx: &mut TxContext,
    ) {
        assert!(tx_context::sender(ctx) == riddle.poser, 2);
        
        let current_epoch = tx_context::epoch(ctx);
        assert!(current_epoch > riddle.created_epoch + riddle.max_epochs, 3);
        
        let Riddle {
            id,
            poser,
            answer_hash: _,
            prize,
            created_epoch: _,
            max_epochs: _,
        } = riddle;
        
        object::delete(id);
        transfer::public_transfer(prize, poser);
    }
}
