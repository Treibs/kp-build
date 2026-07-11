module apiary::hive {
    use std::string::String;

    const ENotOccupied: u64 = 0;
    const ENotKeeper: u64 = 1;

    public struct ApiaryCap has key, store {
        id: UID,
    }

    public struct Apiary has key {
        id: UID,
        occupied_count: u64,
    }

    public struct Stand has key {
        id: UID,
        number: u64,
        keeper: Option<address>,
        queen_line: Option<String>,
        total_weight: u64,
    }

    fun init(ctx: &mut TxContext) {
        transfer::transfer(ApiaryCap { id: object::new(ctx) }, ctx.sender());
        transfer::share_object(Apiary { id: object::new(ctx), occupied_count: 0 });
    }

    public fun create_stand(_cap: &ApiaryCap, number: u64, ctx: &mut TxContext) {
        transfer::share_object(Stand {
            id: object::new(ctx),
            number,
            keeper: option::none(),
            queen_line: option::none(),
            total_weight: 0,
        });
    }

    public fun assign(
        _cap: &ApiaryCap,
        stand: &mut Stand,
        apiary: &mut Apiary,
        keeper_addr: address,
        queen_line: String,
    ) {
        let was_occupied = option::is_some(&stand.keeper);
        stand.keeper = option::some(keeper_addr);
        stand.queen_line = option::some(queen_line);
        if (!was_occupied) {
            apiary.occupied_count = apiary.occupied_count + 1;
        };
    }

    public fun vacate(
        _cap: &ApiaryCap,
        stand: &mut Stand,
        apiary: &mut Apiary,
    ) {
        assert!(option::is_some(&stand.keeper), ENotOccupied);
        stand.keeper = option::none();
        stand.queen_line = option::none();
        apiary.occupied_count = apiary.occupied_count - 1;
    }

    public fun log_weight(stand: &mut Stand, weight: u64, ctx: &TxContext) {
        assert!(option::is_some(&stand.keeper), ENotOccupied);
        assert!(*option::borrow(&stand.keeper) == ctx.sender(), ENotKeeper);
        stand.total_weight = stand.total_weight + weight;
    }

    public fun keeper(stand: &Stand): Option<address> {
        stand.keeper
    }

    public fun queen_line(stand: &Stand): &Option<String> {
        &stand.queen_line
    }

    public fun total_weight(stand: &Stand): u64 {
        stand.total_weight
    }

    public fun occupied_count(apiary: &Apiary): u64 {
        apiary.occupied_count
    }

    public fun number(stand: &Stand): u64 {
        stand.number
    }
}
