module penalty_jar::jar {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::table::{Self, Table};
    use sui::balance::{Self, Balance};
    use sui::event;

    public struct PenaltyJar has key {
        id: UID,
        beneficiary: address,
        fine_amount: u64,
        min_stake: u64,
        pot: u64,
        balance: Balance<SUI>,
        members: Table<address, u64>,
    }

    public struct RefereeCap has key, store {
        id: UID,
    }

    public struct SweptEvent has copy, drop {
        amount: u64,
    }

    public fun create_jar(
        beneficiary: address,
        fine_amount: u64,
        min_stake: u64,
        ctx: &mut TxContext,
    ): RefereeCap {
        let jar = PenaltyJar {
            id: object::new(ctx),
            beneficiary,
            fine_amount,
            min_stake,
            pot: 0,
            balance: balance::zero(),
            members: table::new(ctx),
        };
        transfer::share_object(jar);
        RefereeCap {
            id: object::new(ctx),
        }
    }

    public fun join(
        jar: &mut PenaltyJar,
        stake: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let amount = coin::value(&stake);
        assert!(amount >= jar.min_stake, 0);
        
        let sender = ctx.sender();
        assert!(!table::contains(&jar.members, sender), 1);

        balance::join(&mut jar.balance, coin::into_balance(stake));
        table::add(&mut jar.members, sender, amount);
    }

    public fun top_up(
        jar: &mut PenaltyJar,
        stake: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let amount = coin::value(&stake);
        let sender = ctx.sender();
        assert!(table::contains(&jar.members, sender), 2);

        balance::join(&mut jar.balance, coin::into_balance(stake));
        let current = table::borrow_mut(&mut jar.members, sender);
        *current = *current + amount;
    }

    public fun leave(
        jar: &mut PenaltyJar,
        ctx: &mut TxContext,
    ) {
        let sender = ctx.sender();
        assert!(table::contains(&jar.members, sender), 3);

        let amount = table::remove(&mut jar.members, sender);
        let recovery = coin::from_balance(balance::split(&mut jar.balance, amount), ctx);
        transfer::public_transfer(recovery, sender);
    }

    public fun record_infraction(
        jar: &mut PenaltyJar,
        _cap: &RefereeCap,
        member: address,
    ) {
        assert!(table::contains(&jar.members, member), 4);

        let old_stake = table::remove(&mut jar.members, member);
        let fine = if (old_stake >= jar.fine_amount) {
            jar.fine_amount
        } else {
            old_stake
        };
        
        let new_stake = old_stake - fine;
        jar.pot = jar.pot + fine;

        if (new_stake > 0) {
            table::add(&mut jar.members, member, new_stake);
        }
    }

    public fun sweep(
        jar: &mut PenaltyJar,
        _cap: &RefereeCap,
        ctx: &mut TxContext,
    ) {
        let amount = jar.pot;
        jar.pot = 0;
        let swept = coin::from_balance(balance::split(&mut jar.balance, amount), ctx);
        transfer::public_transfer(swept, jar.beneficiary);
        event::emit(SweptEvent { amount });
    }

    public fun get_stake(jar: &PenaltyJar, member: address): u64 {
        if (table::contains(&jar.members, member)) {
            *table::borrow(&jar.members, member)
        } else {
            0
        }
    }
}
