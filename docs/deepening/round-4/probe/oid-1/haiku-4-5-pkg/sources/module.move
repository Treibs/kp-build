module member::card {
    use sui::object::{Self, UID, ID};
    use sui::event;
    use sui::transfer;
    use sui::tx_context::TxContext;

    public struct MemberCard has key, store {
        id: UID,
        tier: u64,
    }

    public struct ClubCap has key, store {
        id: UID,
    }

    public struct CardRenewed has copy, drop {
        retired_card: ID,
        new_card: ID,
        new_tier: u64,
    }

    public fun issue(_cap: &ClubCap, recipient: address, ctx: &mut TxContext) {
        let card = MemberCard {
            id: object::new(ctx),
            tier: 1,
        };
        transfer::public_transfer(card, recipient);
    }

    public fun renew(old_card: MemberCard, ctx: &mut TxContext): MemberCard {
        let retired_id = object::id(&old_card);
        let new_tier = old_card.tier + 1;
        
        let MemberCard { id, .. } = old_card;
        object::delete(id);
        
        let new_card = MemberCard {
            id: object::new(ctx),
            tier: new_tier,
        };
        
        let new_id = object::id(&new_card);
        
        event::emit(CardRenewed {
            retired_card: retired_id,
            new_card: new_id,
            new_tier,
        });
        
        new_card
    }
}
