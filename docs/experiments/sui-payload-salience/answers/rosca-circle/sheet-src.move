module rotating_circle::circle {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use std::vector;

    public struct SavingsCircle has key {
        id: UID,
        members: vector<address>,
        contribution_amount: u64,
        current_payout_index: u64,
        pot: Coin<SUI>,
        contributed_this_round: vector<bool>,
    }

    const ENotMember: u64 = 1;
    const EAlreadyContributedThisRound: u64 = 2;
    const EWrongContributionAmount: u64 = 3;
    const ENotAllContributed: u64 = 4;

    public fun create_circle(
        members: vector<address>,
        contribution_amount: u64,
        ctx: &mut TxContext,
    ): SavingsCircle {
        let members_count = vector::length(&members);
        let mut contributed_this_round = vector[];
        let mut i = 0;
        while (i < members_count) {
            vector::push_back(&mut contributed_this_round, false);
            i = i + 1;
        };

        SavingsCircle {
            id: object::new(ctx),
            members,
            contribution_amount,
            current_payout_index: 0,
            pot: coin::zero<SUI>(ctx),
            contributed_this_round,
        }
    }

    public fun contribute(
        circle: &mut SavingsCircle,
        contribution: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let sender = tx_context::sender(ctx);
        let members_count = vector::length(&circle.members);
        
        let mut member_index = members_count;
        let mut i = 0;
        while (i < members_count) {
            if (*vector::borrow(&circle.members, i) == sender) {
                member_index = i;
                break
            };
            i = i + 1;
        };
        assert!(member_index < members_count, ENotMember);

        assert!(!*vector::borrow(&circle.contributed_this_round, member_index), EAlreadyContributedThisRound);

        assert!(coin::value(&contribution) == circle.contribution_amount, EWrongContributionAmount);

        *vector::borrow_mut(&mut circle.contributed_this_round, member_index) = true;

        coin::join(&mut circle.pot, contribution);
    }

    public fun trigger_payout(
        circle: &mut SavingsCircle,
        ctx: &mut TxContext,
    ) {
        let members_count = vector::length(&circle.members);
        
        let mut i = 0;
        let mut all_contributed = true;
        while (i < members_count) {
            if (!*vector::borrow(&circle.contributed_this_round, i)) {
                all_contributed = false;
                break
            };
            i = i + 1;
        };
        assert!(all_contributed, ENotAllContributed);

        let recipient = *vector::borrow(&circle.members, circle.current_payout_index);

        let payout_amount = coin::value(&circle.pot);
        let payout = coin::split(&mut circle.pot, payout_amount, ctx);
        transfer::public_transfer(payout, recipient);

        circle.current_payout_index = circle.current_payout_index + 1;

        let mut j = 0;
        while (j < members_count) {
            *vector::borrow_mut(&mut circle.contributed_this_round, j) = false;
            j = j + 1;
        };
    }

    public fun complete_and_cleanup(circle: SavingsCircle) {
        let members_count = vector::length(&circle.members);
        assert!(circle.current_payout_index == members_count, 5);
        assert!(coin::value(&circle.pot) == 0, 5);
        
        let SavingsCircle {
            id,
            members: _,
            contribution_amount: _,
            current_payout_index: _,
            pot,
            contributed_this_round: _,
        } = circle;
        
        object::delete(id);
        coin::destroy_zero(pot);
    }
}
