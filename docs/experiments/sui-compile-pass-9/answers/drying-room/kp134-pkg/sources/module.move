module pottery::drying_room {
    use sui::table::{Table, Self};
    use sui::tx_context::TxContext;

    public struct SlotKey has copy, drop, store {
        bay: u32,
        shelf: u32,
    }

    public struct Piece has copy, drop, store {
        title: vector<u8>,
        owner: address,
    }

    public struct DryingRoom has key {
        id: UID,
        slots: Table<SlotKey, Piece>,
    }

    public fun new(ctx: &mut TxContext): DryingRoom {
        DryingRoom {
            id: object::new(ctx),
            slots: table::new(ctx),
        }
    }

    public fun set_piece(
        room: &mut DryingRoom,
        bay: u32,
        shelf: u32,
        title: vector<u8>,
        ctx: &TxContext,
    ) {
        let key = SlotKey { bay, shelf };
        assert!(!table::contains(&room.slots, key), 1);
        table::add(&mut room.slots, key, Piece {
            title,
            owner: ctx.sender(),
        });
    }

    public fun move_piece(
        room: &mut DryingRoom,
        from_bay: u32,
        from_shelf: u32,
        to_bay: u32,
        to_shelf: u32,
        ctx: &TxContext,
    ) {
        let from_key = SlotKey { bay: from_bay, shelf: from_shelf };
        let to_key = SlotKey { bay: to_bay, shelf: to_shelf };
        
        let piece = table::remove(&mut room.slots, from_key);
        assert!(piece.owner == ctx.sender(), 2);
        assert!(!table::contains(&room.slots, to_key), 3);
        
        table::add(&mut room.slots, to_key, piece);
    }

    public fun take_piece(
        room: &mut DryingRoom,
        bay: u32,
        shelf: u32,
        ctx: &TxContext,
    ): Piece {
        let key = SlotKey { bay, shelf };
        let piece = table::remove(&mut room.slots, key);
        assert!(piece.owner == ctx.sender(), 4);
        piece
    }

    public fun view_piece(
        room: &DryingRoom,
        bay: u32,
        shelf: u32,
    ): (vector<u8>, address) {
        let key = SlotKey { bay, shelf };
        assert!(table::contains(&room.slots, key), 5);
        let piece = table::borrow(&room.slots, key);
        (piece.title, piece.owner)
    }

    public fun piece_count(room: &DryingRoom): u64 {
        table::length(&room.slots)
    }
}
