module loyalty::desk {
    use sui::object;
    use sui::event;

    public struct PointsCard has key, store {
        id: UID,
        balance: u64,
    }

    public struct Merged has copy, drop {
        card_1: address,
        card_2: address,
        new_card: address,
        total_balance: u64,
    }

    public fun create_card(ctx: &mut TxContext): PointsCard {
        PointsCard {
            id: object::new(ctx),
            balance: 0,
        }
    }

    public fun merge(
        card1: PointsCard,
        card2: PointsCard,
        ctx: &mut TxContext,
    ): PointsCard {
        let card1_address = object::id_to_address(&object::id(&card1.id));
        let card2_address = object::id_to_address(&object::id(&card2.id));
        
        let PointsCard { id: id1, balance: bal1 } = card1;
        let PointsCard { id: id2, balance: bal2 } = card2;
        
        let combined_balance = bal1 + bal2;
        
        object::delete(id1);
        object::delete(id2);

        let new_card = PointsCard {
            id: object::new(ctx),
            balance: combined_balance,
        };

        let new_card_address = object::id_to_address(&object::id(&new_card.id));

        event::emit(Merged {
            card_1: card1_address,
            card_2: card2_address,
            new_card: new_card_address,
            total_balance: combined_balance,
        });

        new_card
    }
}
