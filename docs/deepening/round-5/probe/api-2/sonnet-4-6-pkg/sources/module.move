module club::badge_mint {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};

    const ENGRAVER_FEE: u64 = 1_000_000_000;
    const EInsufficientFunds: u64 = 0;

    public struct TreasurerCap has key, store {
        id: UID,
    }

    public struct ClubTreasury has key {
        id: UID,
        balance: Balance<SUI>,
        badges_minted: u64,
        engraver: address,
    }

    public struct Badge has key, store {
        id: UID,
        number: u64,
        member: address,
    }

    fun init(ctx: &mut TxContext) {
        let sender = ctx.sender();
        transfer::transfer(TreasurerCap { id: object::new(ctx) }, sender);
        transfer::share_object(ClubTreasury {
            id: object::new(ctx),
            balance: balance::zero(),
            badges_minted: 0,
            engraver: sender,
        });
    }

    public fun set_engraver(
        _cap: &TreasurerCap,
        treasury: &mut ClubTreasury,
        new_engraver: address,
    ) {
        treasury.engraver = new_engraver;
    }

    public fun pay_dues(treasury: &mut ClubTreasury, payment: Coin<SUI>) {
        coin::put(&mut treasury.balance, payment);
    }

    public fun mint_badge(
        _cap: &TreasurerCap,
        treasury: &mut ClubTreasury,
        member: address,
        ctx: &mut TxContext,
    ) {
        assert!(balance::value(&treasury.balance) >= ENGRAVER_FEE, EInsufficientFunds);
        let fee_balance = balance::split(&mut treasury.balance, ENGRAVER_FEE);
        let fee = coin::from_balance(fee_balance, ctx);
        let engraver = treasury.engraver;
        transfer::public_transfer(fee, engraver);

        treasury.badges_minted = treasury.badges_minted + 1;
        let number = treasury.badges_minted;
        transfer::public_transfer(Badge { id: object::new(ctx), number, member }, member);
    }

    public fun badges_minted(treasury: &ClubTreasury): u64 {
        treasury.badges_minted
    }

    public fun treasury_balance(treasury: &ClubTreasury): u64 {
        balance::value(&treasury.balance)
    }
}
