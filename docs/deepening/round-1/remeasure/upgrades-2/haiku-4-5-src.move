module vault::core {
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;

    public struct Vault has key {
        id: UID,
        balance: Balance<SUI>,
    }

    public fun new(ctx: &mut TxContext): Vault {
        Vault {
            id: object::new(ctx),
            balance: balance::zero(),
        }
    }

    public fun deposit(vault: &mut Vault, coin: Coin<SUI>) {
        balance::join(&mut vault.balance, coin::into_balance(coin));
    }

    public(package) fun withdraw(vault: &mut Vault, amount: u64): Coin<SUI> {
        coin::from_balance(balance::split(&mut vault.balance, amount))
    }
}

module vault::api {
    use vault::core::Vault;
    use sui::transfer;

    public fun withdraw(vault: &mut Vault, amount: u64, ctx: &mut TxContext) {
        let coin = vault::core::withdraw(vault, amount);
        transfer::public_transfer(coin, ctx.sender());
    }
}
