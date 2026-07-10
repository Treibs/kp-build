module apple_press::press {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{TxContext, sender};
    use sui::event;
    use sui::table::{Self, Table};
    use std::vector;
    
    const EAlreadyPressed: u64 = 1;
    const ENotKeeper: u64 = 2;
    const EZeroWeight: u64 = 3;
    
    public struct Press has key {
        id: UID,
        yield_rate: u64,
        pressed: bool,
        keeper: address,
        households: vector<address>,
        weights: Table<address, u64>,
    }
    
    public struct CiderJug has key, store {
        id: UID,
        amount: u64,
    }
    
    public struct DepositEvent has copy, drop {
        household: address,
        weight: u64,
    }
    
    public struct PressedEvent has copy, drop {
        household: address,
        amount: u64,
    }
    
    public struct KeeperShareEvent has copy, drop {
        amount: u64,
    }
    
    public fun create(yield_rate: u64, keeper: address, ctx: &mut TxContext) {
        let press = Press {
            id: object::new(ctx),
            yield_rate,
            pressed: false,
            keeper,
            households: vector::empty(),
            weights: table::new(ctx),
        };
        transfer::share_object(press);
    }
    
    public fun deposit(press: &mut Press, weight: u64, ctx: &mut TxContext) {
        assert!(!press.pressed, EAlreadyPressed);
        
        let household = sender(ctx);
        
        if (table::contains(&press.weights, household)) {
            let current = table::remove(&mut press.weights, household);
            table::add(&mut press.weights, household, current + weight);
        } else {
            vector::push_back(&mut press.households, household);
            table::add(&mut press.weights, household, weight);
        };
        
        event::emit(DepositEvent { household, weight });
    }
    
    public fun weight_waiting(press: &Press): u64 {
        let mut total = 0;
        let mut i = 0;
        let len = vector::length(&press.households);
        
        while (i < len) {
            let household = *vector::borrow(&press.households, i);
            total = total + *table::borrow(&press.weights, household);
            i = i + 1;
        };
        
        total
    }
    
    public fun press(press: &mut Press, ctx: &mut TxContext) {
        assert!(!press.pressed, EAlreadyPressed);
        assert!(sender(ctx) == press.keeper, ENotKeeper);
        
        press.pressed = true;
        
        let total_weight = weight_waiting(press);
        assert!(total_weight > 0, EZeroWeight);
        
        let total_cider = total_weight * press.yield_rate;
        
        let mut distributed = 0;
        let mut i = 0;
        let len = vector::length(&press.households);
        
        while (i < len) {
            let household = *vector::borrow(&press.households, i);
            let household_weight = *table::borrow(&press.weights, household);
            
            let share = (household_weight * total_cider) / total_weight;
            
            let jug = CiderJug {
                id: object::new(ctx),
                amount: share,
            };
            
            transfer::public_transfer(jug, household);
            event::emit(PressedEvent { household, amount: share });
            
            distributed = distributed + share;
            i = i + 1;
        };
        
        let keeper_share = total_cider - distributed;
        let keeper_jug = CiderJug {
            id: object::new(ctx),
            amount: keeper_share,
        };
        
        transfer::public_transfer(keeper_jug, press.keeper);
        event::emit(KeeperShareEvent { amount: keeper_share });
    }
}
