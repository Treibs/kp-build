module payment_channel::channel {
    use std::option::{Self, Option};
    use sui::balance::{Balance, split};
    use sui::coin::{Coin, into_balance, from_balance};
    use sui::event;
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{TxContext, sender, epoch};

    const ENotOpener: u64 = 0;
    const ENotCounterparty: u64 = 1;
    const EAlreadyJoined: u64 = 2;
    const ENotJoined: u64 = 3;
    const EInvalidAmount: u64 = 4;
    const EProposerCannotAccept: u64 = 5;
    const ENotParticipant: u64 = 6;
    const ENotProposer: u64 = 7;
    const ENotEnoughEpochsPassed: u64 = 8;
    const EUnexpectedDeposit: u64 = 9;
    const ENoProposal: u64 = 10;

    public struct ChannelOpened has copy, drop {
        channel_id: ID,
        opener: address,
        counterparty: address,
        opener_deposit: u64,
        epochs_until_force_close: u64,
    }

    public struct CounterpartyJoined has copy, drop {
        channel_id: ID,
        counterparty_deposit: u64,
    }

    public struct ProposalSubmitted has copy, drop {
        channel_id: ID,
        proposer: address,
        proposer_amount: u64,
    }

    public struct ProposalWithdrawn has copy, drop {
        channel_id: ID,
        proposer: address,
    }

    public struct ChannelClosed has copy, drop {
        channel_id: ID,
        opener_amount: u64,
        counterparty_amount: u64,
    }

    public struct Proposal has store {
        proposer: address,
        proposer_amount: u64,
    }

    public struct Channel has key, store {
        id: UID,
        opener: address,
        counterparty: address,
        opener_deposit: Balance<SUI>,
        counterparty_deposit: Option<Balance<SUI>>,
        is_joined: bool,
        proposal: Option<Proposal>,
        opened_epoch: u64,
        epochs_until_force_close: u64,
    }

    public fun open(
        counterparty: address,
        coin: Coin<SUI>,
        epochs_until_force_close: u64,
        ctx: &mut TxContext,
    ) {
        let amount = coin.value();
        let deposit = into_balance(coin);
        let current_epoch = epoch(ctx);
        
        let channel_id = object::new(ctx);
        let channel_id_copy = object::uid_to_inner(&channel_id);
        
        let channel = Channel {
            id: channel_id,
            opener: sender(ctx),
            counterparty,
            opener_deposit: deposit,
            counterparty_deposit: option::none(),
            is_joined: false,
            proposal: option::none(),
            opened_epoch: current_epoch,
            epochs_until_force_close,
        };

        event::emit(ChannelOpened {
            channel_id: channel_id_copy,
            opener: sender(ctx),
            counterparty,
            opener_deposit: amount,
            epochs_until_force_close,
        });

        transfer::share_object(channel);
    }

    public fun join(
        channel: &mut Channel,
        coin: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let caller = sender(ctx);
        assert!(caller == channel.counterparty, ENotCounterparty);
        assert!(!channel.is_joined, EAlreadyJoined);

        let amount = coin.value();
        let deposit = into_balance(coin);

        option::fill(&mut channel.counterparty_deposit, deposit);
        channel.is_joined = true;

        event::emit(CounterpartyJoined {
            channel_id: object::uid_to_inner(&channel.id),
            counterparty_deposit: amount,
        });
    }

    public fun cancel(
        channel: Channel,
        ctx: &mut TxContext,
    ) {
        let caller = sender(ctx);
        assert!(caller == channel.opener, ENotOpener);
        assert!(!channel.is_joined, EAlreadyJoined);

        let Channel {
            id,
            opener,
            opener_deposit,
            counterparty_deposit,
            is_joined,
            proposal,
            ..
        } = channel;

        assert!(option::is_none(&counterparty_deposit), EUnexpectedDeposit);
        option::destroy_none(counterparty_deposit);
        option::destroy_none(proposal);

        object::delete(id);
        
        transfer::public_transfer(
            from_balance(opener_deposit, ctx),
            opener,
        );
    }

    public fun propose_close(
        channel: &mut Channel,
        proposer_amount: u64,
        ctx: &mut TxContext,
    ) {
        let caller = sender(ctx);
        assert!(channel.is_joined, ENotJoined);
        assert!(caller == channel.opener || caller == channel.counterparty, ENotParticipant);
        
        let total = channel.opener_deposit.value() + 
                    option::borrow(&channel.counterparty_deposit).value();
        assert!(proposer_amount <= total, EInvalidAmount);

        let proposal = Proposal {
            proposer: caller,
            proposer_amount,
        };
        
        option::fill(&mut channel.proposal, proposal);

        event::emit(ProposalSubmitted {
            channel_id: object::uid_to_inner(&channel.id),
            proposer: caller,
            proposer_amount,
        });
    }

    public fun accept_close(
        channel: Channel,
        ctx: &mut TxContext,
    ) {
        let caller = sender(ctx);

        let Channel {
            id,
            opener,
            counterparty,
            is_joined,
            mut opener_deposit,
            mut counterparty_deposit,
            mut proposal,
            ..
        } = channel;

        assert!(is_joined, ENotJoined);
        assert!(option::is_some(&proposal), ENoProposal);

        let proposal_val = option::extract(&mut proposal);
        let Proposal { proposer, proposer_amount } = proposal_val;
        
        assert!(caller != proposer, EProposerCannotAccept);
        assert!(caller == opener || caller == counterparty, ENotParticipant);

        let total = opener_deposit.value() + counterparty_deposit.value();
        let other_amount = total - proposer_amount;

        let (opener_payout, counterparty_payout) = if (proposer == opener) {
            (proposer_amount, other_amount)
        } else {
            (other_amount, proposer_amount)
        };

        let mut counterparty_bal = option::extract(&mut counterparty_deposit);
        let opener_coin = from_balance(split(&mut opener_deposit, opener_payout), ctx);
        let counterparty_coin = from_balance(split(&mut counterparty_bal, counterparty_payout), ctx);

        let channel_id_for_event = object::uid_to_inner(&id);
        object::delete(id);

        transfer::public_transfer(opener_coin, opener);
        transfer::public_transfer(counterparty_coin, counterparty);

        event::emit(ChannelClosed {
            channel_id: channel_id_for_event,
            opener_amount: opener_payout,
            counterparty_amount: counterparty_payout,
        });
    }

    public fun withdraw_proposal(
        channel: &mut Channel,
        ctx: &mut TxContext,
    ) {
        let caller = sender(ctx);
        assert!(channel.is_joined, ENotJoined);
        assert!(option::is_some(&channel.proposal), ENoProposal);

        let proposal = option::borrow(&channel.proposal);
        assert!(proposal.proposer == caller, ENotProposer);

        let _ = option::extract(&mut channel.proposal);

        event::emit(ProposalWithdrawn {
            channel_id: object::uid_to_inner(&channel.id),
            proposer: caller,
        });
    }

    public fun force_close(
        channel: Channel,
        ctx: &mut TxContext,
    ) {
        let caller = sender(ctx);

        let Channel {
            id,
            opener,
            counterparty,
            is_joined,
            opener_deposit,
            mut counterparty_deposit,
            opened_epoch,
            epochs_until_force_close,
            ..
        } = channel;

        assert!(is_joined, ENotJoined);
        assert!(caller == opener || caller == counterparty, ENotParticipant);

        let current_epoch = epoch(ctx);
        let required_epochs = opened_epoch + epochs_until_force_close;
        assert!(current_epoch > required_epochs, ENotEnoughEpochsPassed);

        let opener_amount = opener_deposit.value();
        let counterparty_amount = counterparty_deposit.value();
        let mut counterparty_bal = option::extract(&mut counterparty_deposit);

        let channel_id_for_event = object::uid_to_inner(&id);
        object::delete(id);

        transfer::public_transfer(
            from_balance(opener_deposit, ctx),
            opener,
        );
        transfer::public_transfer(
            from_balance(counterparty_bal, ctx),
            counterparty,
        );

        event::emit(ChannelClosed {
            channel_id: channel_id_for_event,
            opener_amount,
            counterparty_amount,
        });
    }
}
