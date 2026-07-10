module insurance::rain_policy {
    use sui::coin::Coin;
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};
    use sui::event;

    public struct Pool has key {
        id: UID,
        vault: Balance<SUI>,
    }

    public struct Policy has key {
        id: UID,
        premium: u64,
        epoch: u64,
    }

    public struct WeatherOracle has key {
        id: UID,
        rainy_epochs: vector<u64>,
    }

    public struct PolicyBought has copy, drop {
        premium: u64,
        epoch: u64,
    }

    public struct PolicySettled has copy, drop {
        payout: u64,
        was_rainy: bool,
    }

    public fun init_pool(ctx: &mut TxContext) {
        let pool = Pool {
            id: object::new(ctx),
            vault: balance::zero<SUI>(),
        };
        transfer::share_object(pool);
    }

    public fun init_oracle(ctx: &mut TxContext) {
        let oracle = WeatherOracle {
            id: object::new(ctx),
            rainy_epochs: vector[],
        };
        transfer::share_object(oracle);
    }

    public fun buy_policy(
        premium: Coin<SUI>,
        epoch: u64,
        pool: &mut Pool,
        ctx: &mut TxContext,
    ): Policy {
        let premium_amount = coin::value(&premium);
        balance::join(&mut pool.vault, coin::into_balance(premium));
        
        event::emit(PolicyBought {
            premium: premium_amount,
            epoch,
        });
        
        Policy {
            id: object::new(ctx),
            premium: premium_amount,
            epoch,
        }
    }

    public fun mark_rainy(oracle: &mut WeatherOracle, epoch: u64) {
        vector::push_back(&mut oracle.rainy_epochs, epoch);
    }

    public fun settle_policy(
        policy: Policy,
        oracle: &WeatherOracle,
        pool: &mut Pool,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let Policy { id, premium, epoch } = policy;
        object::delete(id);
        
        let was_rainy = vector::contains(&oracle.rainy_epochs, &epoch);
        let payout = if (was_rainy) { premium * 2 } else { 0 };
        
        let payout_coin = coin::from_balance(
            balance::split(&mut pool.vault, payout),
            ctx,
        );
        
        event::emit(PolicySettled {
            payout,
            was_rainy,
        });
        
        payout_coin
    }
}
