module ballot::ballot {
    use std::vector;
    use std::string::String;
    use sui::table::{Self, Table};
    use sui::object::ID;
    
    public struct Ballot has key {
        id: UID,
        question: String,
        options: vector<String>,
        votes: vector<u64>,
        voters: Table<address, bool>,
        closed: bool,
    }
    
    public struct ClosingCapability has key, store {
        id: UID,
        ballot_id: ID,
    }
    
    public fun create_ballot(
        question: String,
        options: vector<String>,
        ctx: &mut TxContext,
    ): ClosingCapability {
        let option_count = vector::length(&options);
        let mut votes = vector[];
        let mut i = 0;
        while (i < option_count) {
            vector::push_back(&mut votes, 0);
            i = i + 1;
        };
        
        let ballot = Ballot {
            id: object::new(ctx),
            question,
            options,
            votes,
            voters: table::new(ctx),
            closed: false,
        };
        
        let ballot_id = object::id(&ballot);
        
        let closing_cap = ClosingCapability {
            id: object::new(ctx),
            ballot_id,
        };
        
        transfer::share_object(ballot);
        closing_cap
    }
    
    public fun vote(
        ballot: &mut Ballot,
        option_index: u64,
        ctx: &TxContext,
    ) {
        assert!(!ballot.closed, 1);
        assert!(option_index < vector::length(&ballot.options), 2);
        
        let voter = ctx.sender();
        assert!(!table::contains(&ballot.voters, voter), 3);
        
        let vote_count = vector::borrow_mut(&mut ballot.votes, option_index);
        *vote_count = *vote_count + 1;
        
        table::add(&mut ballot.voters, voter, true);
    }
    
    public fun close_ballot(
        ballot: &mut Ballot,
        cap: &ClosingCapability,
    ) {
        assert!(object::id(ballot) == cap.ballot_id, 4);
        ballot.closed = true;
    }
    
    public fun get_vote_count(ballot: &Ballot, option_index: u64): u64 {
        assert!(option_index < vector::length(&ballot.options), 2);
        *vector::borrow(&ballot.votes, option_index)
    }
    
    public fun get_leading_option(ballot: &Ballot): u64 {
        let option_count = vector::length(&ballot.options);
        assert!(option_count > 0, 5);
        
        let mut max_votes = 0;
        let mut leading_index = 0;
        let mut i = 0;
        
        while (i < option_count) {
            let vote_count = *vector::borrow(&ballot.votes, i);
            if (vote_count > max_votes) {
                max_votes = vote_count;
                leading_index = i;
            };
            i = i + 1;
        };
        
        leading_index
    }
}
