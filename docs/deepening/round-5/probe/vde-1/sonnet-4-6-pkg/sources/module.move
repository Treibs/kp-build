module mailroom::mailroom {
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;

    public struct ClerkCap has key, store {
        id: UID,
    }

    public struct Package has key, store {
        id: UID,
        addressee: address,
    }

    public struct Mailroom has key {
        id: UID,
        intake: vector<Package>,
        pool: Balance<SUI>,
        postage_fee: u64,
    }

    fun init(ctx: &mut TxContext) {
        transfer::transfer(
            ClerkCap { id: object::new(ctx) },
            ctx.sender(),
        );
        transfer::share_object(Mailroom {
            id: object::new(ctx),
            intake: vector[],
            pool: balance::zero(),
            postage_fee: 1_000_000,
        });
    }

    public fun deposit(
        mailroom: &mut Mailroom,
        addressee: address,
        payment: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let paid = coin::into_balance(payment);
        assert!(balance::value(&paid) == mailroom.postage_fee);
        balance::join(&mut mailroom.pool, paid);
        vector::push_back(
            &mut mailroom.intake,
            Package { id: object::new(ctx), addressee },
        );
    }

    public fun dispatch(_cap: &ClerkCap, mailroom: &mut Mailroom) {
        while (!vector::is_empty(&mailroom.intake)) {
            let pkg = vector::pop_back(&mut mailroom.intake);
            let addr = pkg.addressee;
            transfer::public_transfer(pkg, addr);
        };
    }

    public fun packages_waiting(mailroom: &Mailroom): u64 {
        vector::length(&mailroom.intake)
    }

    public fun pool_total(mailroom: &Mailroom): u64 {
        balance::value(&mailroom.pool)
    }
}
