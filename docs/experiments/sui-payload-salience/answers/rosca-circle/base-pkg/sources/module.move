module rotating_savings::circle {
    use sui::object::{Self, UID};
    use sui::tx_context::{Self, TxContext};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::vector;
    use sui::bag::{Self, Bag};
    use sui::transfer;

    struct Circle has key {
        id: UID,
        members: vector<address>,
        contribution_amount: u64,
        current_round: u64,
        current_payout_index: u64,
        total_members: u64,
        payouts_completed: u64,
        contributions_this_round: u64,
        balance: Coin<SUI>,
        contributed_this_round: Bag,
    }

    const ERR_NOT_MEMBER: u64 = 1;
    const ERR_ALREADY_CONTRIBUTED: u64 = 2;
    const ERR_WRONG_AMOUNT: u64 = 3;
    const ERR_NOT_ALL_CONTRIBUTED: u64 = 4;
    const ERR_CIRCLE_NOT_COMPLETE: u64 = 5;

    public fun create_circle(
        members: vector<address>,
        contribution_amount: u64,
        ctx: &mut TxContext,
    ) {
        let total_members = vector::length(&members);
        assert!(total_members > 0, 0);
        
        let circle = Circle {
            id: object::new(ctx),
            members,
            contribution_amount,
            current_round: 0,
            current_payout_index: 0,
            total_members: (total_members as u64),
            payouts_completed: 0,
            contributions_this_round: 0,
            balance: coin::zero(ctx),
            contributed_this_round: bag::new(ctx),
        };
        
        transfer::share_object(circle);
    }

    public fun contribute(
        circle: &mut Circle,
        coin: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let sender = tx_context::sender(ctx);
        
        assert!(vector::contains(&circle.members, &sender), ERR_NOT_MEMBER);
        assert!(!bag::contains(&circle.contributed_this_round, sender), ERR_ALREADY_CONTRIBUTED);
        assert!(coin::value(&coin) == circle.contribution_amount, ERR_WRONG_AMOUNT);
        
        bag::add(&mut circle.contributed_this_round, sender, true);
        circle.contributions_this_round = circle.contributions_this_round + 1;
        coin::join(&mut circle.balance, coin);
    }

    public fun payout(circle: &mut Circle, ctx: &mut TxContext): address {
        assert!(circle.contributions_this_round == circle.total_members, ERR_NOT_ALL_CONTRIBUTED);
        
        let recipient = *vector::borrow(&circle.members, (circle.current_payout_index as u64));
        let payout_amount = coin::value(&circle.balance);
        let payout_coin = coin::split(&mut circle.balance, payout_amount, ctx);
        transfer::public_transfer(payout_coin, recipient);
        
        circle.current_payout_index = (circle.current_payout_index + 1) % circle.total_members;
        circle.current_round = circle.current_round + 1;
        circle.payouts_completed = circle.payouts_completed + 1;
        
        let old_bag = circle.contributed_this_round;
        circle.contributed_this_round = bag::new(ctx);
        circle.contributions_this_round = 0;
        bag::drop(old_bag);
        
        recipient
    }

    public fun complete_and_destroy(circle: Circle) {
        assert!(circle.payouts_completed == circle.total_members, ERR_CIRCLE_NOT_COMPLETE);
        
        let Circle {
            id,
            members: _,
            contribution_amount: _,
            current_round: _,
            current_payout_index: _,
            total_members: _,
            payouts_completed: _,
            contributions_this_round: _,
            balance,
            contributed_this_round,
        } = circle;
        
        object::delete(id);
        coin::destroy_zero(balance);
        bag::drop(contributed_this_round);
    }
}
