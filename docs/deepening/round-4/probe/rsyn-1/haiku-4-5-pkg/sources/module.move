module score::board {
    use sui::table::{Self, Table};

    public struct Scoreboard has key, store {
        id: UID,
        scores: Table<address, u64>,
    }

    public struct RefereeCap has key, store {
        id: UID,
    }

    public fun new(ctx: &mut TxContext): (Scoreboard, RefereeCap) {
        let scoreboard = Scoreboard {
            id: object::new(ctx),
            scores: table::new(ctx),
        };
        let referee_cap = RefereeCap {
            id: object::new(ctx),
        };
        (scoreboard, referee_cap)
    }

    public fun add_point(scoreboard: &mut Scoreboard, player: address, points: u64, _cap: &RefereeCap) {
        if (table::contains(&scoreboard.scores, player)) {
            let current = table::borrow_mut(&mut scoreboard.scores, player);
            *current = *current + points;
        } else {
            table::add(&mut scoreboard.scores, player, points);
        }
    }

    public fun score(scoreboard: &Scoreboard, player: address): u64 {
        if (table::contains(&scoreboard.scores, player)) {
            *table::borrow(&scoreboard.scores, player)
        } else {
            0
        }
    }
}
