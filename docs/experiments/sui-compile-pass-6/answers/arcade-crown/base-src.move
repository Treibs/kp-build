module arcade::high_score_game {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use std::option::{Self, Option};

    public struct Crown has key {
        id: UID,
    }

    public struct HighScoreGame has key {
        id: UID,
        high_score: u64,
        champion: address,
        fee_amount: u64,
    }

    fun init(ctx: &mut TxContext) {
        let crown = Crown {
            id: object::new(ctx),
        };

        let game = HighScoreGame {
            id: object::new(ctx),
            high_score: 0,
            champion: @0x0,
            fee_amount: 1_000_000_000,
        };

        transfer::share_object(game);
        transfer::transfer(crown, tx_context::sender(ctx));
    }

    public fun play(
        game: &mut HighScoreGame,
        score: u64,
        fee: Coin<SUI>,
        crown_opt: Option<Crown>,
        ctx: &mut TxContext,
    ) {
        assert!(coin::value(&fee) >= game.fee_amount, 1);
        
        let player = tx_context::sender(ctx);

        if (score > game.high_score) {
            if (option::is_some(&crown_opt)) {
                let crown = option::extract(&mut crown_opt);
                transfer::transfer(crown, player);
            };
            game.high_score = score;
            game.champion = player;
        } else {
            if (option::is_some(&crown_opt)) {
                let crown = option::extract(&mut crown_opt);
                if (game.champion != @0x0) {
                    transfer::transfer(crown, game.champion);
                } else {
                    transfer::transfer(crown, player);
                };
            };
        };
        
        option::destroy_none(crown_opt);
        transfer::public_transfer(fee, @0x0);
    }
}
