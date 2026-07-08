module payment_channel::payment_channel {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};
    use sui::clock::{Self, Clock};

    const ENotOpener: u64 = 0;
    const ENotCounterparty: u64 = 1;
    const EChannelNotActive: u64 = 2;
    const EInvalidSplit: u64 = 3;
    const ENoPendingProposal: u64 = 4;
    const ENotProposer: u64 = 5;
    const EInsufficientEpochs: u64 = 6;

    const STATE_WAITING: u8 = 0;
    const STATE_ACTIVE: u8 = 1;

    struct PaymentChannel has key {
        id: UID,
        opener: address,
        counterparty: address,
        opener_deposit: Balance<SUI>,
        counterparty_deposit: Balance<SUI>,
        state: u8,
        creation_epoch: u64,
        timeout_epochs: u64,
        proposer: address,
        opener_amount: u64,
        counterparty_amount: u64,
        has_proposal: bool,
    }

    public fun open(
        counterparty: address,
        deposit: Coin<SUI>,
        timeout_epochs: u64,
        clock: &Clock,
        ctx: &mut TxContext,
    ) {
        let opener = tx_context::sender(ctx);
        let creation_epoch = clock::epoch(clock);
        
        let channel = PaymentChannel {
            id: object::new(ctx),
            opener,
            counterparty,
            opener_deposit: coin::into_balance(deposit),
            counterparty_deposit: balance::zero(),
            state: STATE_WAITING,
            creation_epoch,
            timeout_epochs,
            proposer: @0x0,
            opener_amount: 0,
            counterparty_amount: 0,
            has_proposal: false,
        };

        transfer::share_object(channel);
    }

    public fun join(
        channel: &mut PaymentChannel,
        deposit: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let sender = tx_context::sender(ctx);
        assert!(sender == channel.counterparty, ENotCounterparty);
        assert!(channel.state == STATE_WAITING, EChannelNotActive);

        channel.counterparty_deposit = coin::into_balance(deposit);
        channel.state = STATE_ACTIVE;
    }

    public fun cancel(
        channel: PaymentChannel,
        ctx: &mut TxContext,
    ) {
        let sender = tx_context::sender(ctx);
        assert!(sender == channel.opener, ENotOpener);
        assert!(channel.state == STATE_WAITING, EChannelNotActive);

        let PaymentChannel {
            id,
            opener,
            counterparty: _,
            opener_deposit,
            counterparty_deposit: _,
            state: _,
            creation_epoch: _,
            timeout_epochs: _,
            proposer: _,
            opener_amount: _,
            counterparty_amount: _,
            has_proposal: _,
        } = channel;

        object::delete(id);
        let coin = coin::from_balance(opener_deposit, ctx);
        transfer::public_transfer(coin, opener);
    }

    public fun propose_close(
        channel: &mut PaymentChannel,
        opener_amount: u64,
        counterparty_amount: u64,
        ctx: &mut TxContext,
    ) {
        let sender = tx_context::sender(ctx);
        assert!(channel.state == STATE_ACTIVE, EChannelNotActive);
        assert!(
            sender == channel.opener || sender == channel.counterparty,
            ENotOpener,
        );

        let total = balance::value(&channel.opener_deposit) + 
                   balance::value(&channel.counterparty_deposit);
        assert!(opener_amount + counterparty_amount == total, EInvalidSplit);

        channel.proposer = sender;
        channel.opener_amount = opener_amount;
        channel.counterparty_amount = counterparty_amount;
        channel.has_proposal = true;
    }

    public fun accept_close(
        channel: PaymentChannel,
        ctx: &mut TxContext,
    ) {
        let sender = tx_context::sender(ctx);
        assert!(channel.state == STATE_ACTIVE, EChannelNotActive);
        assert!(channel.has_proposal, ENoPendingProposal);
        assert!(sender != channel.proposer, ENotProposer);

        let PaymentChannel {
            id,
            opener,
            counterparty,
            mut opener_deposit,
            mut counterparty_deposit,
            state: _,
            creation_epoch: _,
            timeout_epochs: _,
            proposer: _,
            opener_amount,
            counterparty_amount,
            has_proposal: _,
        } = channel;

        object::delete(id);

        let opener_pay = coin::from_balance(
            balance::split(&mut opener_deposit, opener_amount),
            ctx,
        );
        let counterparty_pay = coin::from_balance(
            balance::split(&mut counterparty_deposit, counterparty_amount),
            ctx,
        );

        transfer::public_transfer(opener_pay, opener);
        transfer::public_transfer(counterparty_pay, counterparty);

        if (balance::value(&opener_deposit) > 0) {
            transfer::public_transfer(coin::from_balance(opener_deposit, ctx), opener);
        } else {
            balance::destroy_zero(opener_deposit);
        };

        if (balance::value(&counterparty_deposit) > 0) {
            transfer::public_transfer(coin::from_balance(counterparty_deposit, ctx), counterparty);
        } else {
            balance::destroy_zero(counterparty_deposit);
        };
    }

    public fun withdraw_proposal(
        channel: &mut PaymentChannel,
        ctx: &mut TxContext,
    ) {
        let sender = tx_context::sender(ctx);
        assert!(channel.has_proposal, ENoPendingProposal);
        assert!(sender == channel.proposer, ENotProposer);

        channel.has_proposal = false;
    }

    public fun force_close(
        channel: PaymentChannel,
        clock: &Clock,
        ctx: &mut TxContext,
    ) {
        let sender = tx_context::sender(ctx);
        assert!(channel.state == STATE_ACTIVE, EChannelNotActive);
        assert!(
            sender == channel.opener || sender == channel.counterparty,
            ENotOpener,
        );

        let current_epoch = clock::epoch(clock);
        assert!(
            current_epoch >= channel.creation_epoch + channel.timeout_epochs,
            EInsufficientEpochs,
        );

        let PaymentChannel {
            id,
            opener,
            counterparty,
            opener_deposit,
            counterparty_deposit,
            state: _,
            creation_epoch: _,
            timeout_epochs: _,
            proposer: _,
            opener_amount: _,
            counterparty_amount: _,
            has_proposal: _,
        } = channel;

        object::delete(id);

        let opener_coin = coin::from_balance(opener_deposit, ctx);
        let counterparty_coin = coin::from_balance(counterparty_deposit, ctx);

        transfer::public_transfer(opener_coin, opener);
        transfer::public_transfer(counterparty_coin, counterparty);
    }
}
