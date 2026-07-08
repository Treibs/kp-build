module auction::english_auction {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use std::option::{Self, Option};

    public struct Artifact has key, store {
        id: UID,
    }

    public struct Auction has key {
        id: UID,
        artifact: Option<Artifact>,
        seller: address,
        min_bid: u64,
        highest_bidder: Option<address>,
        highest_bid: u64,
        highest_bid_coin: Option<Coin<SUI>>,
        is_closed: bool,
    }

    public fun create_artifact(ctx: &mut TxContext): Artifact {
        Artifact {
            id: object::new(ctx),
        }
    }

    public fun start_auction(
        artifact: Artifact,
        min_bid: u64,
        ctx: &mut TxContext,
    ) {
        let auction = Auction {
            id: object::new(ctx),
            artifact: option::some(artifact),
            seller: tx_context::sender(ctx),
            min_bid,
            highest_bidder: option::none(),
            highest_bid: 0,
            highest_bid_coin: option::none(),
            is_closed: false,
        };
        transfer::share_object(auction);
    }

    public fun bid(
        auction: &mut Auction,
        coin: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        assert!(!auction.is_closed, 1);
        assert!(coin::value(&coin) > auction.highest_bid, 2);
        assert!(coin::value(&coin) >= auction.min_bid, 3);

        let sender = tx_context::sender(ctx);

        if (option::is_some(&auction.highest_bidder)) {
            let prev_bidder = option::extract(&mut auction.highest_bidder);
            let prev_coin = option::extract(&mut auction.highest_bid_coin);
            transfer::public_transfer(prev_coin, prev_bidder);
        };

        auction.highest_bidder = option::some(sender);
        auction.highest_bid = coin::value(&coin);
        auction.highest_bid_coin = option::some(coin);
    }

    public fun close_bidding(auction: &mut Auction, ctx: &TxContext) {
        assert!(tx_context::sender(ctx) == auction.seller, 4);
        auction.is_closed = true;
    }

    public fun settle(auction: &mut Auction, ctx: &TxContext) {
        let sender = tx_context::sender(ctx);
        assert!(sender == auction.seller || auction.is_closed, 5);
        
        if (option::is_some(&auction.highest_bidder)) {
            let winner = option::extract(&mut auction.highest_bidder);
            let proceeds = option::extract(&mut auction.highest_bid_coin);
            let artifact = option::extract(&mut auction.artifact);
            
            transfer::public_transfer(artifact, winner);
            transfer::public_transfer(proceeds, auction.seller);
        } else {
            let artifact = option::extract(&mut auction.artifact);
            transfer::public_transfer(artifact, auction.seller);
        };
    }
}
