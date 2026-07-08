module riddle::bounty {
    use sui::object::{Self, UID};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::transfer;
    use sui::tx_context::TxContext;
    use sui::clock::Clock;
    use sui::event;
    use std::hash;

    const EWrongAnswer: u64 = 0;
    const ENotPoser: u64 = 1;
    const ETimeoutNotReached: u64 = 2;

    const EPOCH_MS: u64 = 86400000;

    public struct Riddle has key, store {
        id: UID,
        answer_hash: vector<u8>,
        prize: Coin<SUI>,
        poser: address,
        created_ms: u64,
        timeout_epochs: u64,
    }

    public struct Solved has copy, drop {
        solver: address,
        prize_amount: u64,
    }

    public struct Reclaimed has copy, drop {
        prize_amount: u64,
    }

    public fun create(
        answer: vector<u8>,
        prize_coin: Coin<SUI>,
        timeout_epochs: u64,
        clock: &Clock,
        ctx: &mut TxContext,
    ) {
        let answer_hash = hash::sha2_256(&answer);

        transfer::share_object(Riddle {
            id: object::new(ctx),
            answer_hash,
            prize: prize_coin,
            poser: ctx.sender(),
            created_ms: clock.timestamp_ms(),
            timeout_epochs,
        });
    }

    public fun solve(
        riddle: Riddle,
        submitted_answer: vector<u8>,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let submitted_hash = hash::sha2_256(&submitted_answer);
        assert!(submitted_hash == riddle.answer_hash, EWrongAnswer);

        let Riddle {
            id,
            prize,
            ..
        } = riddle;

        let prize_amount = coin::value(&prize);

        event::emit(Solved {
            solver: ctx.sender(),
            prize_amount,
        });

        object::delete(id);
        prize
    }

    public fun reclaim(
        riddle: Riddle,
        clock: &Clock,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        assert!(riddle.poser == ctx.sender(), ENotPoser);

        let elapsed_ms = clock.timestamp_ms() - riddle.created_ms;
        let elapsed_epochs = elapsed_ms / EPOCH_MS;
        assert!(elapsed_epochs > riddle.timeout_epochs, ETimeoutNotReached);

        let Riddle {
            id,
            prize,
            ..
        } = riddle;

        let prize_amount = coin::value(&prize);

        event::emit(Reclaimed {
            prize_amount,
        });

        object::delete(id);
        prize
    }
}
