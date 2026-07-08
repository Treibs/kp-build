module savings_circle::circle {
    use std::vector;
    use sui::coin::{Self, Coin};
    use sui::object;
    use sui::sui::SUI;
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};

    public struct SavingsCircle has key {
        id: UID,
        members: vector<address>,
        contribution_amount: u64,
        payout_index: u64,
        contributed: vector<bool>,
        pot: Coin<SUI>,
    }

    public fun create_circle(
        members: vector<address>,
        contribution_amount: u64,
        ctx: &mut TxContext,
    ) {
        assert!(vector::length(&members) > 0, 0);
        
        let mut contributed = vector[];
        let mut i = 0;
        while (i < vector::length(&members)) {
            contributed.push_back(false);
            i = i + 1;
        };

        let circle = SavingsCircle {
            id: object::new(ctx),
            members,
            contribution_amount,
            payout_index: 0,
            contributed,
            pot: coin::zero(ctx),
        };

        transfer::share_object(circle);
    }

    public fun contribute(
        circle: &mut SavingsCircle,
        payment: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let sender = tx_context::sender(ctx);
        
        assert!(payment.value() == circle.contribution_amount, 1);
        
        let mut member_index = vector::length(&circle.members);
        let mut i = 0;
        while (i < vector::length(&circle.members)) {
            if (*vector::borrow(&circle.members, i) == sender) {
                member_index = i;
                break
            };
            i = i + 1;
        };
        assert!(member_index < vector::length(&circle.members), 2);
        
        let already_contributed = *vector::borrow(&circle.contributed, member_index);
        assert!(!already_contributed, 3);
        
        let contributed_ref = vector::borrow_mut(&mut circle.contributed, member_index);
        *contributed_ref = true;
        coin::join(&mut circle.pot, payment);
    }

    fun do_payout(circle: &mut SavingsCircle, ctx: &mut TxContext) {
        let all_contributed = vector::all(&circle.contributed, |contributed| contributed);
        assert!(all_contributed, 4);
        
        let recipient = *vector::borrow(&circle.members, circle.payout_index);
        
        let payout_amount = circle.contribution_amount * vector::length(&circle.members);
        let payout = coin::split(&mut circle.pot, payout_amount, ctx);
        
        transfer::public_transfer(payout, recipient);
        
        let mut i = 0;
        while (i < vector::length(&circle.contributed)) {
            let ref = vector::borrow_mut(&mut circle.contributed, i);
            *ref = false;
            i = i + 1;
        };
        
        circle.payout_index = circle.payout_index + 1;
    }

    public fun trigger_payout(circle: &mut SavingsCircle, ctx: &mut TxContext) {
        assert!(circle.payout_index < vector::length(&circle.members), 5);
        do_payout(circle, ctx);
    }

    public fun trigger_final_payout_and_cleanup(mut circle: SavingsCircle, ctx: &mut TxContext) {
        assert!(circle.payout_index + 1 == vector::length(&circle.members), 6);
        do_payout(&mut circle, ctx);
        let SavingsCircle { id, members: _, contribution_amount: _, payout_index: _, contributed: _, pot } = circle;
        coin::destroy_zero(pot);
        object::delete(id);
    }
}
