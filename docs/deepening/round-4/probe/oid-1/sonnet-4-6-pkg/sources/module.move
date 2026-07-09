module member::card {
    use sui::event;

    public struct ClubCap has key, store {
        id: UID,
    }

    public struct MemberCard has key {
        id: UID,
        tier: u64,
    }

    public struct CardRenewed has copy, drop {
        retired_id: ID,
        successor_id: ID,
        new_tier: u64,
    }

    fun init(ctx: &mut TxContext) {
        let cap = ClubCap { id: object::new(ctx) };
        transfer::transfer(cap, ctx.sender());
    }

    public fun issue(_cap: &ClubCap, recipient: address, ctx: &mut TxContext) {
        let card = MemberCard { id: object::new(ctx), tier: 1 };
        transfer::transfer(card, recipient);
    }

    public fun renew(old_card: MemberCard, ctx: &mut TxContext) {
        let new_tier = old_card.tier + 1;
        let retired_id = object::id(&old_card);
        let MemberCard { id, tier: _ } = old_card;
        object::delete(id);

        let new_card = MemberCard { id: object::new(ctx), tier: new_tier };
        let successor_id = object::id(&new_card);

        event::emit(CardRenewed { retired_id, successor_id, new_tier });

        transfer::transfer(new_card, ctx.sender());
    }
}
