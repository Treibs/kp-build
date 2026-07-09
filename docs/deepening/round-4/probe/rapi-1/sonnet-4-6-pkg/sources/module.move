module duel::record {
    use sui::table::{Self, Table};

    public struct ScorekeeperCap has key, store {
        id: UID,
    }

    public struct Pair has copy, drop, store {
        winner: address,
        loser: address,
    }

    public struct DuelLedger has key {
        id: UID,
        scores: Table<Pair, u64>,
    }

    fun init(ctx: &mut TxContext) {
        transfer::transfer(ScorekeeperCap { id: object::new(ctx) }, ctx.sender());
        transfer::share_object(DuelLedger {
            id: object::new(ctx),
            scores: table::new(ctx),
        });
    }

    public fun record_win(
        _cap: &ScorekeeperCap,
        ledger: &mut DuelLedger,
        winner: address,
        loser: address,
    ) {
        let pair = Pair { winner, loser };
        if (table::contains(&ledger.scores, pair)) {
            let count = table::borrow_mut(&mut ledger.scores, pair);
            *count = *count + 1;
        } else {
            table::add(&mut ledger.scores, pair, 1);
        };
    }

    public fun wins(ledger: &DuelLedger, winner: address, loser: address): u64 {
        let pair = Pair { winner, loser };
        if (table::contains(&ledger.scores, pair)) {
            *table::borrow(&ledger.scores, pair)
        } else {
            0
        }
    }
}
