module rank::ladder {
    use std::vector;

    public struct Entry has copy, drop, store {
        player: address,
        score: u64,
    }

    public struct Ladder has key {
        id: UID,
        entries: vector<Entry>,
    }

    public struct GymCap has key, store {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        let gym_cap = GymCap {
            id: object::new(ctx),
        };
        transfer::transfer(gym_cap, ctx.sender());

        let ladder = Ladder {
            id: object::new(ctx),
            entries: vector[],
        };
        transfer::share_object(ladder);
    }

    public fun submit_score(
        ladder: &mut Ladder,
        player: address,
        score: u64,
        _cap: &GymCap,
    ) {
        let mut i = 0;
        let len = vector::length(&ladder.entries);

        while (i < len) {
            let entry = vector::borrow(&ladder.entries, i);
            if (entry.score < score) {
                vector::insert(&mut ladder.entries, Entry { player, score }, i);
                return
            };
            i = i + 1;
        };

        vector::push_back(&mut ladder.entries, Entry { player, score });
    }

    public fun position(ladder: &Ladder, player: address): u64 {
        let mut i = 0;
        let len = vector::length(&ladder.entries);

        while (i < len) {
            let entry = vector::borrow(&ladder.entries, i);
            if (entry.player == player) {
                return i + 1
            };
            i = i + 1;
        };

        abort 0
    }

    public fun podium(ladder: &Ladder): vector<address> {
        let mut result = vector[];
        let len = vector::length(&ladder.entries);
        let mut i = 0;

        while (i < 3 && i < len) {
            let entry = vector::borrow(&ladder.entries, i);
            vector::push_back(&mut result, entry.player);
            i = i + 1;
        };

        result
    }
}
