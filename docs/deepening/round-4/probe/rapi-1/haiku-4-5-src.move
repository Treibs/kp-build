module duel::record {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::TxContext;
    use sui::table::{Self, Table};

    public struct DuelKey has copy, drop, store {
        winner: address,
        loser: address,
    }

    public struct DuelLedger has key {
        id: UID,
        wins: Table<DuelKey, u64>,
    }

    public struct ScorekeeperCap has key, store {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        let ledger = DuelLedger {
            id: object::new(ctx),
            wins: table::new(ctx),
        };
        let cap = ScorekeeperCap {
            id: object::new(ctx),
        };

        transfer::share_object(ledger);
        transfer::transfer(cap, ctx.sender());
    }

    public fun record_win(
        ledger: &mut DuelLedger,
        winner: address,
        loser: address,
        _cap: &ScorekeeperCap,
    ) {
        let key = DuelKey { winner, loser };
        let current = if (table::contains(&ledger.wins, key)) {
            table::remove(&mut ledger.wins, key)
        } else {
            0
        };
        table::add(&mut ledger.wins, key, current + 1);
    }

    public fun wins(ledger: &DuelLedger, winner: address, loser: address): u64 {
        let key = DuelKey { winner, loser };
        if (table::contains(&ledger.wins, key)) {
            *table::borrow(&ledger.wins, key)
        } else {
            0
        }
    }
}
