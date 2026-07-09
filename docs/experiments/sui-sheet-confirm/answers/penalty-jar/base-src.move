module penalty_jar::jar {
    use sui::object::{Self, UID};
    use sui::tx_context::{Self, TxContext};
    use sui::transfer;
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::vec_map::{Self, VecMap};
    use sui::event;

    const EMinimumStakeNotMet: u64 = 1;
    const EAlreadyMember: u64 = 2;
    const ENotMember: u64 = 3;

    public struct RefereeCapability has key {
        id: UID,
    }

    public struct MemberStake has store {
        balance: Balance<SUI>,
    }

    public struct PenaltyJar has key {
        id: UID,
        beneficiary: address,
        fine_amount: u64,
        minimum_stake: u64,
        pot: Balance<SUI>,
        members: VecMap<address, MemberStake>,
    }

    public struct MemberJoined has copy, drop {
        member: address,
        stake: u64,
    }

    public struct InfractionRecorded has copy, drop {
        member: address,
        fine: u64,
        removed: bool,
    }

    public struct MemberLeft has copy, drop {
        member: address,
        recovered: u64,
    }

    public struct PotSwept has copy, drop {
        amount: u64,
        beneficiary: address,
    }

    public struct StakeTopUp has copy, drop {
        member: address,
        amount: u64,
        new_total: u64,
    }

    public fun create_jar(
        beneficiary: address,
        fine_amount: u64,
        minimum_stake: u64,
        ctx: &mut TxContext,
    ) {
        let jar = PenaltyJar {
            id: object::new(ctx),
            beneficiary,
            fine_amount,
            minimum_stake,
            pot: balance::zero(),
            members: vec_map::empty(),
        };

        let capability = RefereeCapability {
            id: object::new(ctx),
        };

        transfer::share_object(jar);
        transfer::transfer(capability, tx_context::sender(ctx));
    }

    public fun join(
        jar: &mut PenaltyJar,
        stake: Coin<SUI>,
        ctx: &TxContext,
    ) {
        let sender = tx_context::sender(ctx);
        let stake_amount = coin::value(&stake);

        assert!(stake_amount >= jar.minimum_stake, EMinimumStakeNotMet);
        assert!(!vec_map::contains(&jar.members, &sender), EAlreadyMember);

        let stake_balance = coin::into_balance(stake);
        vec_map::insert(&mut jar.members, sender, MemberStake {
            balance: stake_balance,
        });

        event::emit(MemberJoined {
            member: sender,
            stake: stake_amount,
        });
    }

    public fun get_stake(jar: &PenaltyJar, member: address): u64 {
        let member_stake = vec_map::get(&jar.members, &member);
        balance::value(&member_stake.balance)
    }

    public fun top_up(
        jar: &mut PenaltyJar,
        member: address,
        additional_stake: Coin<SUI>,
    ) {
        let amount = coin::value(&additional_stake);
        let member_stake = vec_map::get_mut(&mut jar.members, &member);
        let additional_balance = coin::into_balance(additional_stake);
        balance::join(&mut member_stake.balance, additional_balance);

        event::emit(StakeTopUp {
            member,
            amount,
            new_total: balance::value(&member_stake.balance),
        });
    }

    public fun record_infraction(
        jar: &mut PenaltyJar,
        _capability: &RefereeCapability,
        member: address,
    ) {
        assert!(vec_map::contains(&jar.members, &member), ENotMember);

        let member_stake = vec_map::get_mut(&mut jar.members, &member);
        let current_stake = balance::value(&member_stake.balance);
        let fine = jar.fine_amount;

        if (current_stake >= fine) {
            let fine_amount = balance::split(&mut member_stake.balance, fine);
            balance::join(&mut jar.pot, fine_amount);

            event::emit(InfractionRecorded {
                member,
                fine,
                removed: false,
            });
        } else {
            let (_member, member_stake_obj) = vec_map::remove(&mut jar.members, &member);
            let remaining_balance = member_stake_obj.balance;
            let remaining = balance::value(&remaining_balance);
            balance::join(&mut jar.pot, remaining_balance);

            event::emit(InfractionRecorded {
                member,
                fine: remaining,
                removed: true,
            });
        }
    }

    public fun leave(
        jar: &mut PenaltyJar,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let sender = tx_context::sender(ctx);
        assert!(vec_map::contains(&jar.members, &sender), ENotMember);

        let (_member, member_stake_obj) = vec_map::remove(&mut jar.members, &sender);
        let balance = member_stake_obj.balance;
        let stake_amount = balance::value(&balance);

        event::emit(MemberLeft {
            member: sender,
            recovered: stake_amount,
        });

        coin::from_balance(balance, ctx)
    }

    public fun sweep_pot(
        jar: &mut PenaltyJar,
        _capability: &RefereeCapability,
        ctx: &mut TxContext,
    ) {
        let amount = balance::value(&jar.pot);
        let pot = balance::split(&mut jar.pot, amount);

        transfer::public_transfer(
            coin::from_balance(pot, ctx),
            jar.beneficiary,
        );

        event::emit(PotSwept {
            amount,
            beneficiary: jar.beneficiary,
        });
    }
}
