module marina::waitlist {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::TxContext;
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};
    use std::vector;
    use std::option::{Self, Option};

    public struct Marina has key {
        id: UID,
        berths: vector<Berth>,
        waitlist: vector<WaitlistEntry>,
        deposits: Balance<SUI>,
    }

    public struct Berth has store {
        length: u64,
        available: bool,
        held_deposit: u64,
    }

    public struct WaitlistEntry has store {
        applicant: address,
        boat_length: u64,
    }

    public struct AdminCap has key, store {
        id: UID,
    }

    public struct WaitlistInfo has copy, drop {
        applicant: address,
        boat_length: u64,
    }

    fun init(ctx: &mut TxContext) {
        let admin_cap = AdminCap {
            id: object::new(ctx),
        };
        transfer::transfer(admin_cap, ctx.sender());

        let marina = Marina {
            id: object::new(ctx),
            berths: vector[],
            waitlist: vector[],
            deposits: balance::zero(),
        };
        transfer::share_object(marina);
    }

    public fun apply(marina: &mut Marina, boat_length: u64, ctx: &mut TxContext) {
        let entry = WaitlistEntry {
            applicant: ctx.sender(),
            boat_length,
        };
        vector::push_back(&mut marina.waitlist, entry);
    }

    public fun add_berth(marina: &mut Marina, length: u64, _cap: &AdminCap) {
        let berth = Berth {
            length,
            available: true,
            held_deposit: 0,
        };
        vector::push_back(&mut marina.berths, berth);
    }

    public fun free_berth(marina: &mut Marina, _cap: &AdminCap, berth_index: u64) {
        let berth = vector::borrow_mut(&mut marina.berths, berth_index);
        berth.available = true;
        berth.held_deposit = 0;
    }

    public fun assign_berth(
        marina: &mut Marina,
        berth_index: u64,
        waitlist_index: u64,
        deposit: Coin<SUI>,
        _cap: &AdminCap,
    ) {
        let _entry = vector::remove(&mut marina.waitlist, waitlist_index);
        let amount = coin::value(&deposit);
        balance::join(&mut marina.deposits, coin::into_balance(deposit));
        
        let berth = vector::borrow_mut(&mut marina.berths, berth_index);
        berth.available = false;
        berth.held_deposit = amount;
    }

    public fun next_waitlist_entry(marina: &Marina): Option<WaitlistInfo> {
        if (vector::length(&marina.waitlist) > 0) {
            let entry = vector::borrow(&marina.waitlist, 0);
            option::some(WaitlistInfo {
                applicant: entry.applicant,
                boat_length: entry.boat_length,
            })
        } else {
            option::none()
        }
    }

    public fun get_berth_deposit(marina: &Marina, berth_index: u64): u64 {
        if (berth_index < vector::length(&marina.berths)) {
            let berth = vector::borrow(&marina.berths, berth_index);
            berth.held_deposit
        } else {
            0
        }
    }
}
