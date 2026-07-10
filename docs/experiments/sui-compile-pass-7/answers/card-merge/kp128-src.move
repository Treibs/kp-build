module loyalty_desk::loyalty {
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;
    use sui::transfer;
    use sui::event;

    public struct DeskCap has key, store {
        id: UID,
    }

    public struct PointsCard has key, store {
        id: UID,
        balance: u64,
    }

    public struct Merged has copy, drop {
        card1_id: object::ID,
        card2_id: object::ID,
        new_card_id: object::ID,
        total_balance: u64,
    }

    fun init(ctx: &mut TxContext) {
        let cap = DeskCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, ctx.sender());
    }

    public fun merge(
        card1: PointsCard,
        card2: PointsCard,
        _cap: &DeskCap,
        ctx: &mut TxContext,
    ): PointsCard {
        let PointsCard { id: id1, balance: balance1 } = card1;
        let PointsCard { id: id2, balance: balance2 } = card2;

        let total_balance = balance1 + balance2;
        let new_card = PointsCard {
            id: object::new(ctx),
            balance: total_balance,
        };

        let card1_id = object::uid_to_inner(&id1);
        let card2_id = object::uid_to_inner(&id2);
        let new_card_id = object::id(&new_card);

        object::delete(id1);
        object::delete(id2);

        event::emit(Merged {
            card1_id,
            card2_id,
            new_card_id,
            total_balance,
        });

        new_card
    }
}
