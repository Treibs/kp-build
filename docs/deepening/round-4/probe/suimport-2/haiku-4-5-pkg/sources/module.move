module raffle::pot {
    use sui::coin::{Coin, join, split, zero, value};
    use sui::sui::SUI;
    use sui::tx_context::sender;
    use std::vector;

    public struct OrganizerCap has key, store {
        id: UID,
    }

    public struct Raffle has key {
        id: UID,
        ticket_price: u64,
        pot: Coin<SUI>,
        entrants: vector<address>,
    }

    fun init(ctx: &mut TxContext) {
        let cap = OrganizerCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, sender(ctx));
    }

    public fun create(ticket_price: u64, ctx: &mut TxContext) {
        let raffle = Raffle {
            id: object::new(ctx),
            ticket_price,
            pot: zero<SUI>(ctx),
            entrants: vector[],
        };
        transfer::share_object(raffle);
    }

    public fun enter(raffle: &mut Raffle, payment: Coin<SUI>, ctx: &mut TxContext) {
        assert!(value(&payment) == raffle.ticket_price, 0);
        join(&mut raffle.pot, payment);
        vector::push_back(&mut raffle.entrants, sender(ctx));
    }

    public fun draw(_cap: &OrganizerCap, raffle: &mut Raffle, winner_index: u64, ctx: &mut TxContext) {
        assert!(winner_index < vector::length(&raffle.entrants), 0);
        let winner = *vector::borrow(&raffle.entrants, winner_index);
        let prize = split(&mut raffle.pot, value(&raffle.pot), ctx);
        transfer::public_transfer(prize, winner);
        raffle.entrants = vector[];
    }
}
