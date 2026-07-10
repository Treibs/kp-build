module loyalty::cards {
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;
    use sui::event;

    public struct PointsCard has key {
        id: UID,
        points: u64,
    }

    public struct MergedEvent has copy, drop {
        old_card_1: address,
        old_card_2: address,
        new_card: address,
        combined_points: u64,
    }

    public struct LoyaltyDesk has key {
        id: UID,
    }

    public fun create_card(points: u64, ctx: &mut TxContext): PointsCard {
        PointsCard {
            id: object::new(ctx),
            points,
        }
    }

    public fun merge_cards(
        card_1: PointsCard,
        card_2: PointsCard,
        _desk: &LoyaltyDesk,
        ctx: &mut TxContext,
    ): PointsCard {
        let combined_points = card_1.points + card_2.points;
        let old_card_1 = object::id(&card_1).to_address();
        let old_card_2 = object::id(&card_2).to_address();
        
        let new_card = PointsCard {
            id: object::new(ctx),
            points: combined_points,
        };
        
        let new_card_addr = object::id(&new_card).to_address();
        
        event::emit(MergedEvent {
            old_card_1,
            old_card_2,
            new_card: new_card_addr,
            combined_points,
        });
        
        let PointsCard { id: id1, points: _ } = card_1;
        let PointsCard { id: id2, points: _ } = card_2;
        object::delete(id1);
        object::delete(id2);
        
        new_card
    }

    public fun create_loyalty_desk(ctx: &mut TxContext): LoyaltyDesk {
        LoyaltyDesk {
            id: object::new(ctx),
        }
    }
}
