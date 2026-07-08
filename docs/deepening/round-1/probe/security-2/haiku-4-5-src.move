module handover::handover {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};

    public struct Estate has key, store {
        id: UID,
        value: u64,
    }

    public struct Offer has key, store {
        id: UID,
        estate: Estate,
        original_owner: address,
        recipient: address,
    }

    public fun create_estate(value: u64, ctx: &mut TxContext): Estate {
        Estate {
            id: object::new(ctx),
            value,
        }
    }

    public fun offer(estate: Estate, to: address, ctx: &mut TxContext) {
        let offer = Offer {
            id: object::new(ctx),
            estate,
            original_owner: tx_context::sender(ctx),
            recipient: to,
        };
        transfer::public_transfer(offer, to);
    }

    public fun accept(offer: Offer, _ctx: &mut TxContext): Estate {
        let Offer { id, estate, original_owner: _, recipient: _ } = offer;
        object::delete(id);
        estate
    }

    public fun decline(offer: Offer, _ctx: &mut TxContext) {
        let Offer { id, estate, original_owner, recipient: _ } = offer;
        object::delete(id);
        transfer::public_transfer(estate, original_owner);
    }
}
