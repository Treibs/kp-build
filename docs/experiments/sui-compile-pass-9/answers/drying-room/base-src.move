module pottery_studio::drying_room {
    use std::string::String;
    use sui::object::{Self, UID};
    use sui::tx_context::{Self, TxContext};
    use sui::table::{Self, Table};
    use sui::transfer;

    const ESlotOccupied: u64 = 1;
    const ESlotEmpty: u64 = 2;
    const ENotOwner: u64 = 3;

    struct Slot has store {
        bay: u32,
        shelf: u32,
        piece_title: String,
        owner: address,
    }

    struct DryingRoom has key {
        id: UID,
        slots: Table<(u32, u32), Slot>,
        total_pieces: u32,
    }

    public fun create_drying_room(ctx: &mut TxContext) {
        let drying_room = DryingRoom {
            id: object::new(ctx),
            slots: table::new(ctx),
            total_pieces: 0,
        };
        transfer::share_object(drying_room);
    }

    public fun set_piece(
        drying_room: &mut DryingRoom,
        bay: u32,
        shelf: u32,
        piece_title: String,
        ctx: &mut TxContext,
    ) {
        let key = (bay, shelf);
        assert!(!table::contains(&drying_room.slots, key), ESlotOccupied);

        let slot = Slot {
            bay,
            shelf,
            piece_title,
            owner: tx_context::sender(ctx),
        };

        table::add(&mut drying_room.slots, key, slot);
        drying_room.total_pieces = drying_room.total_pieces + 1;
    }

    public fun move_piece(
        drying_room: &mut DryingRoom,
        from_bay: u32,
        from_shelf: u32,
        to_bay: u32,
        to_shelf: u32,
        ctx: &mut TxContext,
    ) {
        let from_key = (from_bay, from_shelf);
        let to_key = (to_bay, to_shelf);

        assert!(table::contains(&drying_room.slots, from_key), ESlotEmpty);
        assert!(!table::contains(&drying_room.slots, to_key), ESlotOccupied);

        {
            let slot = table::borrow(&drying_room.slots, from_key);
            assert!(slot.owner == tx_context::sender(ctx), ENotOwner);
        };

        let Slot { bay: _, shelf: _, piece_title, owner } = 
            table::remove(&mut drying_room.slots, from_key);
        
        let new_slot = Slot {
            bay: to_bay,
            shelf: to_shelf,
            piece_title,
            owner,
        };
        table::add(&mut drying_room.slots, to_key, new_slot);
    }

    public fun take_down(
        drying_room: &mut DryingRoom,
        bay: u32,
        shelf: u32,
        ctx: &mut TxContext,
    ) {
        let key = (bay, shelf);
        assert!(table::contains(&drying_room.slots, key), ESlotEmpty);

        {
            let slot = table::borrow(&drying_room.slots, key);
            assert!(slot.owner == tx_context::sender(ctx), ENotOwner);
        };

        let _slot = table::remove(&mut drying_room.slots, key);
        drying_room.total_pieces = drying_room.total_pieces - 1;
    }

    public fun get_piece_info(
        drying_room: &DryingRoom,
        bay: u32,
        shelf: u32,
    ): (String, address) {
        let key = (bay, shelf);
        assert!(table::contains(&drying_room.slots, key), ESlotEmpty);

        let slot = table::borrow(&drying_room.slots, key);
        (slot.piece_title, slot.owner)
    }

    public fun get_total_pieces(drying_room: &DryingRoom): u32 {
        drying_room.total_pieces
    }
}
