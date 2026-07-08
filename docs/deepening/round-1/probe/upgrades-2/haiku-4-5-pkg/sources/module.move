module vault::core {
    use sui::balance::{self, Balance};
    use sui::coin::{self, Coin};
    use sui::sui::SUI;

    public struct Vault has key {
        id: UID,
        balance: Balance<SUI>,
    }

    public fun deposit(vault: &mut Vault, coin: Coin<SUI>) {
        balance::join(&mut vault.balance, coin::into_balance(coin));
    }

    public(package) fun withdraw_internal(vault: &mut Vault, amount: u64, ctx: &mut TxContext): Coin<SUI> {
        coin::from_balance(balance::split(&mut vault.balance, amount), ctx)
    }
}

module vault::api {
    use vault::core;

    public fun withdraw(vault: &mut core::Vault, amount: u64, ctx: &mut TxContext) {
        let coin = core::withdraw_internal(vault, amount, ctx);
        transfer::public_transfer(coin, ctx.sender());
    }
}
