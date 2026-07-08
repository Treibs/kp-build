module payment_channel::channel {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::event;
    use std::option::{Self, Option};

    public struct Channel has key {
        id: UID,
        opener: address,
        counterparty: address,
        opener_deposit: u64,
        counterparty_deposit: u64,
        counterparty_joined: bool,
        created_epoch: u64,
        max_force_close_epochs: u64,
        proposal: Option<Proposal>,
        opener_coin: Coin<SUI>,
        counterparty_coin: Option<Coin<SUI>>,
    }

    public struct Proposal has store, copy, drop {
        proposer: address,
        opener_amount: u64,
        counterparty_amount: u64,
    }

    public struct ChannelOpened has copy, drop {
        channel_id: ID,
        opener: address,
        counterparty: address,
        opener_deposit: u64,
    }

    public struct ChannelJoined has copy, drop {
        channel_id: ID,
        counterparty: address,
        counterparty_deposit: u64,
    }

    public struct ProposalMade has copy, drop {
        channel_id: ID,
        proposer: address,
        opener_amount: u64,
        counterparty_amount: u64,
    }

    public struct ProposalAccepted has copy, drop {
        channel_id: ID,
        opener_amount: u64,
        counterparty_amount: u64,
    }

    public struct ForceCloseEvent has copy, drop {
        channel_id: ID,
        opener_amount: u64,
        counterparty_amount: u64,
    }

    public struct ChannelCanceled has copy, drop {
        channel_id: ID,
        opener_deposit: u64,
    }

    public fun create(
        counterparty: address,
        deposit: Coin<SUI>,
        max_force_close_epochs: u64,
        ctx: &mut TxContext
    ) {
        let id = object::new(ctx);
        let opener = tx_context::sender(ctx);
        let opener_deposit = coin::value(&deposit);
        let created_epoch = tx_context::epoch(ctx);
        
        let channel = Channel {
            id,
            opener,
            counterparty,
            opener_deposit,
            counterparty_deposit: 0,
            counterparty_joined: false,
            created_epoch,
            max_force_close_epochs,
            proposal: option::none(),
            opener_coin: deposit,
            counterparty_coin: option::none(),
        };
        
        event::emit(ChannelOpened {
            channel_id: object::uid_to_inner(&channel.id),
            opener,
            counterparty,
            opener_deposit,
        });
        
        transfer::share_object(channel);
    }

    public fun join(
        channel: &mut Channel,
        deposit: Coin<SUI>,
        ctx: &mut TxContext
    ) {
        assert!(!channel.counterparty_joined, 1);
        assert!(tx_context::sender(ctx) == channel.counterparty, 2);
        
        let counterparty_deposit = coin::value(&deposit);
        channel.counterparty_deposit = counterparty_deposit;
        channel.counterparty_joined = true;
        channel.counterparty_coin = option::some(deposit);
        
        event::emit(ChannelJoined {
            channel_id: object::uid_to_inner(&channel.id),
            counterparty: channel.counterparty,
            counterparty_deposit,
        });
    }

    public fun cancel(
        channel: Channel,
        ctx: &mut TxContext
    ) {
        assert!(!channel.counterparty_joined, 3);
        assert!(tx_context::sender(ctx) == channel.opener, 4);
        
        let Channel {
            id,
            opener,
            counterparty: _,
            opener_deposit,
            counterparty_deposit: _,
            counterparty_joined: _,
            created_epoch: _,
            max_force_close_epochs: _,
            proposal: _,
            opener_coin,
            counterparty_coin: _,
        } = channel;
        
        transfer::public_transfer(opener_coin, opener);
        
        event::emit(ChannelCanceled {
            channel_id: object::uid_to_inner(&id),
            opener_deposit,
        });
        
        object::delete(id);
    }

    public fun propose_close(
        channel: &mut Channel,
        opener_amount: u64,
        counterparty_amount: u64,
        ctx: &mut TxContext
    ) {
        assert!(channel.counterparty_joined, 5);
        assert!(opener_amount + counterparty_amount == channel.opener_deposit + channel.counterparty_deposit, 6);
        
        let sender = tx_context::sender(ctx);
        assert!(sender == channel.opener || sender == channel.counterparty, 7);
        
        let proposal = Proposal {
            proposer: sender,
            opener_amount,
            counterparty_amount,
        };
        
        channel.proposal = option::some(proposal);
        
        event::emit(ProposalMade {
            channel_id: object::uid_to_inner(&channel.id),
            proposer: sender,
            opener_amount,
            counterparty_amount,
        });
    }

    public fun withdraw_proposal(
        channel: &mut Channel,
        ctx: &mut TxContext
    ) {
        let sender = tx_context::sender(ctx);
        let proposal = option::borrow(&channel.proposal);
        
        assert!(sender == proposal.proposer, 8);
        
        channel.proposal = option::none();
    }

    public fun accept_close(
        mut channel: Channel,
        ctx: &mut TxContext
    ) {
        assert!(channel.counterparty_joined, 9);
        assert!(option::is_some(&channel.proposal), 10);
        
        let sender = tx_context::sender(ctx);
        let proposal_ref = option::borrow(&channel.proposal);
        
        assert!(sender != proposal_ref.proposer, 11);
        
        let prop = option::extract(&mut channel.proposal);
        let cp_coin = option::extract(&mut channel.counterparty_coin);
        
        let Channel {
            id,
            opener,
            counterparty,
            opener_deposit: _,
            counterparty_deposit: _,
            counterparty_joined: _,
            created_epoch: _,
            max_force_close_epochs: _,
            proposal: _,
            opener_coin,
            counterparty_coin: _,
        } = channel;
        
        let mut combined = opener_coin;
        coin::join(&mut combined, cp_coin);
        
        let opener_payout = coin::split(&mut combined, prop.opener_amount, ctx);
        transfer::public_transfer(opener_payout, opener);
        transfer::public_transfer(combined, counterparty);
        
        event::emit(ProposalAccepted {
            channel_id: object::uid_to_inner(&id),
            opener_amount: prop.opener_amount,
            counterparty_amount: prop.counterparty_amount,
        });
        
        object::delete(id);
    }

    public fun force_close(
        mut channel: Channel,
        ctx: &mut TxContext
    ) {
        assert!(channel.counterparty_joined, 12);
        
        let sender = tx_context::sender(ctx);
        assert!(sender == channel.opener || sender == channel.counterparty, 13);
        
        let current_epoch = tx_context::epoch(ctx);
        assert!(current_epoch >= channel.created_epoch + channel.max_force_close_epochs, 14);
        
        let cp_coin = option::extract(&mut channel.counterparty_coin);
        
        let Channel {
            id,
            opener,
            counterparty,
            opener_deposit,
            counterparty_deposit,
            counterparty_joined: _,
            created_epoch: _,
            max_force_close_epochs: _,
            proposal: _,
            opener_coin,
            counterparty_coin: _,
        } = channel;
        
        let mut combined = opener_coin;
        coin::join(&mut combined, cp_coin);
        
        let opener_payout = coin::split(&mut combined, opener_deposit, ctx);
        transfer::public_transfer(opener_payout, opener);
        transfer::public_transfer(combined, counterparty);
        
        event::emit(ForceCloseEvent {
            channel_id: object::uid_to_inner(&id),
            opener_amount: opener_deposit,
            counterparty_amount: counterparty_deposit,
        });
        
        object::delete(id);
    }
}
