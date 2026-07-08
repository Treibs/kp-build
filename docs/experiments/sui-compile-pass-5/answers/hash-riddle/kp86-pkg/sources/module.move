module 0x0::riddle_bounty {
    use sui::hash;
    use sui::coin::{Coin, SUI, Self};
    use sui::balance::{Balance, Self};
    use sui::event;
    use sui::object::{Self, UID, ID};
    use sui::transfer;
    use sui::tx_context::TxContext;

    public struct Riddle has key, store {
        id: UID,
        poser: address,
        prize: Balance<SUI>,
        answer_hash: vector<u8>,
        created_epoch: u64,
        expiration_epochs: u64,
    }

    public struct RiddleCreated has copy, drop {
        riddle_id: ID,
        poser: address,
        prize_amount: u64,
    }

    public struct RiddleSolved has copy, drop {
        riddle_id: ID,
        solver: address,
        prize_amount: u64,
    }

    public struct RiddleReclaimed has copy, drop {
        riddle_id: ID,
        poser: address,
        prize_amount: u64,
    }

    public fun create(
        answer: vector<u8>,
        prize: Coin<SUI>,
        expiration_epochs: u64,
        ctx: &mut TxContext,
    ) {
        let answer_hash = hash::blake2b256(&answer);
        let prize_amount = coin::value(&prize);
        
        let riddle = Riddle {
            id: object::new(ctx),
            poser: ctx.sender(),
            prize: coin::into_balance(prize),
            answer_hash,
            created_epoch: ctx.epoch(),
            expiration_epochs,
        };
        
        let riddle_id = object::id(&riddle);
        
        event::emit(RiddleCreated {
            riddle_id,
            poser: ctx.sender(),
            prize_amount,
        });
        
        transfer::share_object(riddle);
    }

    public fun solve(
        riddle: Riddle,
        answer: vector<u8>,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let answer_hash = hash::blake2b256(&answer);
        assert!(answer_hash == riddle.answer_hash, 0);
        
        let riddle_id = object::id(&riddle);
        
        let Riddle {
            id,
            poser: _,
            prize,
            answer_hash: _,
            created_epoch: _,
            expiration_epochs: _,
        } = riddle;
        
        let prize_coin = coin::from_balance(prize, ctx);
        let prize_amount = coin::value(&prize_coin);
        
        event::emit(RiddleSolved {
            riddle_id,
            solver: ctx.sender(),
            prize_amount,
        });
        
        object::delete(id);
        prize_coin
    }

    public fun reclaim(
        riddle: Riddle,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        assert!(ctx.sender() == riddle.poser, 1);
        assert!(ctx.epoch() >= riddle.created_epoch + riddle.expiration_epochs, 2);
        
        let riddle_id = object::id(&riddle);
        
        let Riddle {
            id,
            poser,
            prize,
            answer_hash: _,
            created_epoch: _,
            expiration_epochs: _,
        } = riddle;
        
        let prize_amount = balance::value(&prize);
        let prize_coin = coin::from_balance(prize, ctx);
        
        event::emit(RiddleReclaimed {
            riddle_id,
            poser,
            prize_amount,
        });
        
        object::delete(id);
        prize_coin
    }
}
