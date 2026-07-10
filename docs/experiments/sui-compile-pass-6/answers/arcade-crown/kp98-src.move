module arcade::highscore {
    use std::option::{Option, some, is_some, extract, fill};
    use sui::coin::{Coin, SUI};
    use sui::balance::Balance;
    use sui::event;
    
    const EInsufficientFee: u64 = 1;
    const ENotOperator: u64 = 2;
    const ECrownAlreadyInGame: u64 = 3;
    
    public struct Crown has key, store {
        id: UID,
    }
    
    public struct Game has key {
        id: UID,
        high_score: u64,
        champion: address,
        crown: Option<Crown>,
        fee: u64,
        operator: address,
        fees: Balance<SUI>,
    }
    
    public struct NewChampion has copy, drop {
        player: address,
        score: u64,
    }
    
    fun init(ctx: &mut TxContext) {
        let crown = Crown { id: object::new(ctx) };
        let game = Game {
            id: object::new(ctx),
            high_score: 0,
            champion: @0x0,
            crown: some(crown),
            fee: 1_000_000_000,
            operator: ctx.sender(),
            fees: balance::zero(),
        };
        transfer::share_object(game);
    }
    
    public fun play(
        game: &mut Game,
        score: u64,
        mut payment: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        assert!(coin::value(&payment) >= game.fee, EInsufficientFee);
        
        let fee_coin = coin::split(&mut payment, game.fee, ctx);
        coin::put(&mut game.fees, fee_coin);
        
        if (coin::value(&payment) > 0) {
            transfer::public_transfer(payment, ctx.sender());
        } else {
            coin::destroy_zero(payment);
        };
        
        if (score > game.high_score) {
            game.high_score = score;
            game.champion = ctx.sender();
            
            if (is_some(&game.crown)) {
                let crown = extract(&mut game.crown);
                transfer::public_transfer(crown, ctx.sender());
            };
            
            event::emit(NewChampion {
                player: ctx.sender(),
                score,
            });
        }
    }
    
    public fun return_crown(
        game: &mut Game,
        crown: Crown,
    ) {
        assert!(!is_some(&game.crown), ECrownAlreadyInGame);
        fill(&mut game.crown, crown);
    }
    
    public fun sweep_fees(
        game: &mut Game,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        assert!(ctx.sender() == game.operator, ENotOperator);
        let amount = balance::value(&game.fees);
        coin::from_balance(balance::split(&mut game.fees, amount), ctx)
    }
}
