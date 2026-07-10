module awards::fulfillment {
    use sui::object::{Self, UID, ID};
    use sui::transfer;
    use sui::tx_context::TxContext;
    use sui::event;
    use sui::table::{Self, Table};

    public struct Shipped has copy, drop {
        winner: address,
    }

    public struct Trophy has key, store {
        id: UID,
        winner: address,
    }

    public struct Desk has key {
        id: UID,
        shipped: Table<ID, address>,
    }

    public struct DeskCap has key, store {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        let desk = Desk {
            id: object::new(ctx),
            shipped: table::new(ctx),
        };
        transfer::share_object(desk);

        let cap = DeskCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, ctx.sender());
    }

    public fun create_trophy(winner: address, ctx: &mut TxContext): Trophy {
        Trophy {
            id: object::new(ctx),
            winner,
        }
    }

    public fun ship_trophy(desk: &mut Desk, _cap: &DeskCap, trophy: Trophy) {
        let winner = trophy.winner;
        let trophy_id = object::uid_to_inner(&trophy.id);
        
        table::add(&mut desk.shipped, trophy_id, winner);
        event::emit(Shipped { winner });
        transfer::public_transfer(trophy, winner);
    }

    public fun is_shipped(desk: &Desk, trophy_id: ID): bool {
        table::contains(&desk.shipped, trophy_id)
    }
}
