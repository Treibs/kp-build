module petty_cash::petty_cash {
    use sui::sui::SUI;
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};
    use sui::transfer;
    use sui::table::{Self, Table};
    use sui::event;

    public struct Drawer has key, store {
        id: UID,
        department: u64,
        balance: Balance<SUI>,
    }

    public struct FacilitiesRegistry has key {
        id: UID,
        drawer_count: u64,
        drawers: Table<u64, address>,
    }

    public struct FacilitiesCap has key {
        id: UID,
    }

    public struct DrawerOpened has copy, drop {
        department: u64,
        drawer_id: address,
    }

    fun init(ctx: &mut TxContext) {
        let registry = FacilitiesRegistry {
            id: object::new(ctx),
            drawer_count: 0,
            drawers: table::new(ctx),
        };
        transfer::share_object(registry);

        let cap = FacilitiesCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, ctx.sender());
    }

    public fun open_drawer(
        _cap: &FacilitiesCap,
        department: u64,
        registry: &mut FacilitiesRegistry,
        ctx: &mut TxContext,
    ) {
        let drawer = Drawer {
            id: object::new(ctx),
            department,
            balance: balance::zero(),
        };

        let drawer_id = object::uid_to_address(&drawer.id);
        table::add(&mut registry.drawers, department, drawer_id);
        registry.drawer_count = registry.drawer_count + 1;

        event::emit(DrawerOpened {
            department,
            drawer_id,
        });

        transfer::share_object(drawer);
    }

    public fun fund_drawer(drawer: &mut Drawer, funds: Coin<SUI>) {
        balance::join(&mut drawer.balance, coin::into_balance(funds));
    }

    public fun transfer_between(
        _cap: &FacilitiesCap,
        from: &mut Drawer,
        to: &mut Drawer,
        amount: u64,
    ) {
        let withdrawn = balance::split(&mut from.balance, amount);
        balance::join(&mut to.balance, withdrawn);
    }

    public fun get_balance(drawer: &Drawer): u64 {
        balance::value(&drawer.balance)
    }

    public fun total_open_drawers(registry: &FacilitiesRegistry): u64 {
        registry.drawer_count
    }

    public fun drawer_exists(registry: &FacilitiesRegistry, department: u64): bool {
        table::contains(&registry.drawers, department)
    }

    public fun get_drawer_address(registry: &FacilitiesRegistry, department: u64): address {
        *table::borrow(&registry.drawers, department)
    }
}
