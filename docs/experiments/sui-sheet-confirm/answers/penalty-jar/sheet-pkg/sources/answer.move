module penalty_jar::penalty_jar {
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::transfer;
    use sui::event;
    use sui::dynamic_field;

    const ENotMember: u64 = 1;
    const EAlreadyMember: u64 = 2;
    const EInsufficientStake: u64 = 3;

    public struct PenaltyJar has key, store {
        id: UID,
        beneficiary: address,
        fine_amount: u64,
        minimum_stake: u64,
        pot: Balance<SUI>,
    }

    public struct RefereeCap has key, store {
        id: UID,
    }

    public struct MemberJoined has copy, drop {
        member: address,
        stake: u64,
    }

    public struct InfractionRecorded has copy, drop {
        member: address,
        fine: u64,
        remaining_stake: u64,
        member_removed: bool,
    }

    public struct MemberLeft has copy, drop {
        member: address,
        stake: u64,
    }

    public struct PotSwept has copy, drop {
        amount: u64,
    }

    public fun create_jar(
        beneficiary: address,
        fine_amount: u64,
        minimum_stake: u64,
        ctx: &mut TxContext,
    ): RefereeCap {
        let jar = PenaltyJar {
            id: object::new(ctx),
            beneficiary,
            fine_amount,
            minimum_stake,
            pot: balance::zero(),
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
        let member = ctx.sender();
        let stake_amount = stake.value();

        assert!(stake_amount >= jar.minimum_stake, EInsufficientStake);
        assert!(!dynamic_field::exists(&jar.id, member), EAlreadyMember);

        let balance = stake.into_balance();
        dynamic_field::add(&mut jar.id, member, balance);

        event::emit(MemberJoined {
            member,
            stake: stake_amount,
        });
    }

    public fun top_up(
        jar: &mut PenaltyJar,
        additional_stake: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let member = ctx.sender();
        assert!(dynamic_field::exists(&jar.id, member), ENotMember);

        let member_balance: &mut Balance<SUI> = dynamic_field::borrow_mut(&mut jar.id, member);
        let additional_balance = additional_stake.into_balance();
        member_balance.join(additional_balance);
    }

    public fun record_infraction(
        _cap: &RefereeCap,
        jar: &mut PenaltyJar,
        member: address,
    ) {
        assert!(dynamic_field::exists(&jar.id, member), ENotMember);

        let member_balance: &mut Balance<SUI> = dynamic_field::borrow_mut(&mut jar.id, member);
        let current_stake = member_balance.value();
        let fine = if (current_stake >= jar.fine_amount) {
            jar.fine_amount
        } else {
            current_stake
        };

        let fine_balance = member_balance.split(fine);
        jar.pot.join(fine_balance);

        let remaining_stake = member_balance.value();
        let member_removed = remaining_stake == 0;

        if (member_removed) {
            let removed_balance: Balance<SUI> = dynamic_field::remove(&mut jar.id, member);
            removed_balance.destroy_zero();
        }

        event::emit(InfractionRecorded {
            member,
            fine,
            remaining_stake,
            member_removed,
        });
    }

    public fun leave(
        jar: &mut PenaltyJar,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let member = ctx.sender();
        assert!(dynamic_field::exists(&jar.id, member), ENotMember);

        let member_balance: Balance<SUI> = dynamic_field::remove(&mut jar.id, member);
        let stake = member_balance.value();

        event::emit(MemberLeft {
            member,
            stake,
        });

        coin::from_balance(member_balance, ctx)
    }

    public fun sweep_pot(
        _cap: &RefereeCap,
        jar: &mut PenaltyJar,
        ctx: &mut TxContext,
    ) {
        let amount = jar.pot.value();
        let swept_balance = jar.pot.split(amount);
        transfer::public_transfer(
            coin::from_balance(swept_balance, ctx),
            jar.beneficiary,
        );

        event::emit(PotSwept { amount });
    }

    public fun member_stake(
        jar: &PenaltyJar,
        member: address,
    ): u64 {
        if (dynamic_field::exists(&jar.id, member)) {
            let member_balance: &Balance<SUI> = dynamic_field::borrow(&jar.id, member);
            member_balance.value()
        } else {
            0
        }
    }
}
