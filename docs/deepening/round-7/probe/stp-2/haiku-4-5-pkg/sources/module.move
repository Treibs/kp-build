module transit::pass {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::table::{Self, Table};
    use sui::balance::{Self, Balance};

    public struct Pass has key, store {
        id: UID,
        holder: address,
        zones: u64,
        rides_remaining: u64,
    }

    public struct InspectorCap has key {
        id: UID,
    }

    public struct Authority has key {
        id: UID,
        ride_price: u64,
        revenue: Balance<SUI>,
        valid_passes: Table<address, bool>,
    }

    public struct PASS has drop {}

    fun init(otw: PASS, ctx: &mut TxContext) {
        let inspector = InspectorCap {
            id: object::new(ctx),
        };
        
        let authority = Authority {
            id: object::new(ctx),
            ride_price: 1_000_000,
            revenue: balance::zero(),
            valid_passes: table::new(ctx),
        };
        
        transfer::share_object(authority);
        transfer::transfer(inspector, ctx.sender());
    }

    public fun create_pass(
        authority: &mut Authority,
        holder: address,
        zones: u64,
        initial_rides: u64,
        ctx: &mut TxContext,
    ) {
        let pass = Pass {
            id: object::new(ctx),
            holder,
            zones,
            rides_remaining: initial_rides,
        };
        
        table::add(&mut authority.valid_passes, holder, true);
        transfer::transfer(pass, holder);
    }

    public fun topup_rides(
        authority: &mut Authority,
        pass: &mut Pass,
        num_rides: u64,
        mut payment: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        let cost = (num_rides as u128) * (authority.ride_price as u128);
        assert!((coin::value(&payment) as u128) >= cost, 0);
        
        pass.rides_remaining = pass.rides_remaining + num_rides;
        
        let paid = coin::split(&mut payment, (cost as u64), ctx);
        balance::join(&mut authority.revenue, coin::into_balance(paid));
        
        if (coin::value(&payment) > 0) {
            transfer::public_transfer(payment, pass.holder);
        } else {
            coin::destroy_zero(payment);
        };
    }

    public fun void_pass(
        authority: &mut Authority,
        pass: Pass,
        _inspector: &InspectorCap,
    ) {
        let Pass { id, holder, zones: _, rides_remaining: _ } = pass;
        if (table::contains(&authority.valid_passes, holder)) {
            table::remove(&mut authority.valid_passes, holder);
        };
        object::delete(id);
    }

    public fun rides_remaining(pass: &Pass): u64 {
        pass.rides_remaining
    }

    public fun zones(pass: &Pass): u64 {
        pass.zones
    }

    public fun has_valid_pass(authority: &Authority, holder: address): bool {
        table::contains(&authority.valid_passes, holder)
    }

    public fun ride_price(authority: &Authority): u64 {
        authority.ride_price
    }
}
