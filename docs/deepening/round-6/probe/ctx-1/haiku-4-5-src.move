module onboarding::team {
    use sui::sui::SUI;
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::TxContext;

    public struct TEAM has drop {}

    public struct AdminCap has key, store {
        id: UID,
    }

    public struct Registry has key {
        id: UID,
        member_count: u64,
    }

    public struct Wallet has key, store {
        id: UID,
        balance: Balance<SUI>,
        jersey_number: u64,
        owner: address,
    }

    fun init(_witness: TEAM, ctx: &mut TxContext) {
        let registry = Registry {
            id: object::new(ctx),
            member_count: 0,
        };
        
        let admin_cap = AdminCap {
            id: object::new(ctx),
        };
        
        transfer::share_object(registry);
        transfer::transfer(admin_cap, ctx.sender());
    }

    public fun onboard_member(
        _admin_cap: &AdminCap,
        registry: &mut Registry,
        jersey_number: u64,
        owner: address,
        ctx: &mut TxContext,
    ): Wallet {
        let wallet = Wallet {
            id: object::new(ctx),
            balance: balance::zero(),
            jersey_number,
            owner,
        };
        
        registry.member_count = registry.member_count + 1;
        
        wallet
    }

    public fun topup_wallet(wallet: &mut Wallet, coin: Coin<SUI>) {
        let coin_balance = coin::into_balance(coin);
        balance::join(&mut wallet.balance, coin_balance);
    }

    public fun get_balance(wallet: &Wallet): u64 {
        balance::value(&wallet.balance)
    }

    public fun get_jersey_number(wallet: &Wallet): u64 {
        wallet.jersey_number
    }

    public fun get_owner(wallet: &Wallet): address {
        wallet.owner
    }

    public fun get_member_count(registry: &Registry): u64 {
        registry.member_count
    }
}
