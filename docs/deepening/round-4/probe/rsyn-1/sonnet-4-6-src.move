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
        let board = Scoreboard {
            id: object::new(ctx),
            scores: table::new(ctx),
        };
        let cap = RefereeCap {
            id: object::new(ctx),
        };
        (board, cap)
    }

    public fun add_point(board: &mut Scoreboard, _cap: &RefereeCap, player: address, amount: u64) {
        if (table::contains(&board.scores, player)) {
            let current = table::borrow_mut(&mut board.scores, player);
            *current = *current + amount;
        } else {
            table::add(&mut board.scores, player, amount);
        }
    }

    public fun score(board: &Scoreboard, player: address): u64 {
        if (table::contains(&board.scores, player)) {
            *table::borrow(&board.scores, player)
        } else {
            0
        }
    }
}
