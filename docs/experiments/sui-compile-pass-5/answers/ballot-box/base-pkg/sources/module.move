module ballot::ballot {
    use std::string::String;
    use std::vector;
    use sui::object::{Self, UID, ID};
    use sui::tx_context::{Self, TxContext};
    use sui::transfer;
    use sui::table::{Self, Table};

    public struct Ballot has key {
        id: UID,
        question: String,
        options: vector<String>,
        votes: Table<u64, u64>,
        voters: Table<address, bool>,
        closed: bool,
    }

    public struct ClosingCapability has key {
        id: UID,
        ballot_id: ID,
    }

    public fun create_ballot(
        question: String,
        options: vector<String>,
        ctx: &mut TxContext,
    ): ClosingCapability {
        let ballot_uid = object::new(ctx);
        let ballot_id = object::uid_to_inner(&ballot_uid);
        
        let mut ballot = Ballot {
            id: ballot_uid,
            question,
            options,
            votes: table::new(ctx),
            voters: table::new(ctx),
            closed: false,
        };

        let mut i = 0;
        while (i < vector::length(&ballot.options)) {
            table::add(&mut ballot.votes, i, 0u64);
            i = i + 1;
        };

        transfer::share_object(ballot);

        ClosingCapability {
            id: object::new(ctx),
            ballot_id,
        }
    }

    public fun vote(
        ballot: &mut Ballot,
        option_index: u64,
        ctx: &TxContext,
    ) {
        let voter = tx_context::sender(ctx);
        
        assert!(!ballot.closed, 1);
        assert!(option_index < vector::length(&ballot.options), 2);
        assert!(!table::contains(&ballot.voters, voter), 3);
        
        let current = table::borrow_mut(&mut ballot.votes, option_index);
        *current = *current + 1;
        
        table::add(&mut ballot.voters, voter, true);
    }

    public fun close_ballot(
        ballot: &mut Ballot,
        cap: ClosingCapability,
    ) {
        assert!(cap.ballot_id == object::uid_to_inner(&ballot.id), 4);
        ballot.closed = true;
        
        let ClosingCapability { id, ballot_id: _ } = cap;
        object::delete(id);
    }

    public fun get_vote_count(
        ballot: &Ballot,
        option_index: u64,
    ): u64 {
        assert!(option_index < vector::length(&ballot.options), 2);
        *table::borrow(&ballot.votes, option_index)
    }

    public fun get_leading_option(
        ballot: &Ballot,
    ): u64 {
        let mut max_votes = 0u64;
        let mut leading_index = 0u64;
        let mut i = 0u64;
        let options_len = vector::length(&ballot.options);
        
        while (i < options_len) {
            let votes = *table::borrow(&ballot.votes, i);
            if (votes > max_votes) {
                max_votes = votes;
                leading_index = i;
            };
            i = i + 1;
        };
        
        leading_index
    }
}
