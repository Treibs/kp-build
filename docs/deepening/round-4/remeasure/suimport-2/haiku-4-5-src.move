module raffle::pot {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::tx_context::{Self, TxContext};
    use sui::dynamic_field;
    use std::vector;

    public struct OrganizerCap has key, store {
        id: UID,
    }

    public struct Raffle has key {
        id: UID,
        ticket_price: u64,
        entrants: vector<address>,
    }

    fun init(ctx: &mut TxContext) {
        let cap = OrganizerCap { id: object::new(ctx) };
        transfer::transfer(cap, tx_context::sender(ctx));
    }

    public fun create_raffle(ticket_price: u64, ctx: &mut TxContext) {
        let mut raffle = Raffle {
            id: object::new(ctx),
            ticket_price,
            entrants: vector[],
        };
        
        dynamic_field::add(&mut raffle.id, b"pot", coin::zero<SUI>(ctx));
        transfer::share_object(raffle);
    }

    public fun enter(raffle: &mut Raffle, payment: Coin<SUI>, ctx: &mut TxContext) {
        let amount = coin::value(&payment);
        assert!(amount == raffle.ticket_price, 1);
        
        let pot: &mut Coin<SUI> = dynamic_field::borrow_mut(&mut raffle.id, b"pot");
        coin::join(pot, payment);
        
        vector::push_back(&mut raffle.entrants, tx_context::sender(ctx));
    }

    public fun draw(_cap: &OrganizerCap, raffle: &mut Raffle, winner_index: u64, ctx: &mut TxContext) {
        let num_entrants = vector::length(&raffle.entrants);
        assert!(winner_index < num_entrants, 2);
        
        let winner = vector::remove(&mut raffle.entrants, winner_index);
        let pot_coin: Coin<SUI> = dynamic_field::remove(&mut raffle.id, b"pot");
        
        dynamic_field::add(&mut raffle.id, b"pot", coin::zero<SUI>(ctx));
        transfer::public_transfer(pot_coin, winner);
    }
}
