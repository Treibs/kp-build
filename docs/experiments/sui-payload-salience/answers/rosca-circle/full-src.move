module rotating_circle::circle {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::table::{Self, Table};
    use sui::event;
    use std::vector;
    use std::option::{Self, Option};

    public struct Circle has key, store {
        id: UID,
        members: vector<address>,
        contribution_amount: u64,
        current_round: u64,
        current_payout_index: u64,
        last_contribution_round: Table<address, u64>,
        pot: Option<Coin<SUI>>,
    }

    public struct ContributionMade has copy, drop {
        member: address,
        round: u64,
    }

    public struct PayoutDistributed has copy, drop {
        round: u64,
        recipient: address,
    }

    public struct CircleCompleted has copy, drop {
        num_members: u64,
    }

    public fun create_circle(
        members: vector<address>,
        contribution_amount: u64,
        ctx: &mut TxContext,
    ) {
        let circle = Circle {
            id: object::new(ctx),
            members,
            contribution_amount,
            current_round: 0,
            current_payout_index: 0,
            last_contribution_round: table::new(ctx),
            pot: option::none(),
        };

        transfer::share_object(circle);
    }

    public fun contribute(
        circle: &mut Circle,
        contribution: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let sender = ctx.sender();
        
        assert!(vector::contains(&circle.members, &sender), 1);
        assert!(coin::value(&contribution) == circle.contribution_amount, 2);

        if (table::contains(&circle.last_contribution_round, sender)) {
            let last_round = *table::borrow(&circle.last_contribution_round, sender);
            assert!(last_round != circle.current_round, 3);
        };

        if (table::contains(&circle.last_contribution_round, sender)) {
            *table::borrow_mut(&mut circle.last_contribution_round, sender) = circle.current_round;
        } else {
            table::add(&mut circle.last_contribution_round, sender, circle.current_round);
        };

        if (option::is_none(&circle.pot)) {
            option::fill(&mut circle.pot, contribution);
        } else {
            coin::join(option::borrow_mut(&mut circle.pot), contribution);
        };

        event::emit(ContributionMade {
            member: sender,
            round: circle.current_round,
        });
    }

    public fun distribute_payout(circle: &mut Circle, ctx: &mut TxContext): Coin<SUI> {
        let members_len = vector::length(&circle.members);
        
        let mut i = 0;
        while (i < members_len) {
            let member = *vector::borrow(&circle.members, i);
            assert!(table::contains(&circle.last_contribution_round, member), 4);
            let last_round = *table::borrow(&circle.last_contribution_round, member);
            assert!(last_round == circle.current_round, 4);
            i = i + 1;
        };

        let recipient = *vector::borrow(&circle.members, circle.current_payout_index);
        let payout_amount = circle.contribution_amount * (members_len as u64);

        let payout = coin::split(option::borrow_mut(&mut circle.pot), payout_amount, ctx);

        event::emit(PayoutDistributed {
            round: circle.current_round,
            recipient,
        });

        circle.current_round = circle.current_round + 1;
        circle.current_payout_index = circle.current_payout_index + 1;

        if (circle.current_payout_index == members_len) {
            event::emit(CircleCompleted {
                num_members: members_len as u64,
            });
        };

        payout
    }

    public fun cleanup(circle: Circle) {
        let members_len = vector::length(&circle.members);
        assert!(circle.current_payout_index == members_len, 5);

        let Circle {
            id,
            members: _,
            contribution_amount: _,
            current_round: _,
            current_payout_index: _,
            last_contribution_round,
            mut pot,
        } = circle;

        if (option::is_some(&pot)) {
            let remaining_coin = option::extract(&mut pot);
            coin::destroy_zero(remaining_coin);
        };

        table::destroy_empty(last_contribution_round);
        object::delete(id);
    }
}
