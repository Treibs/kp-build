module car_ferry::manifest {
    use sui::coin::{Self, Coin};
    use sui::balance::{Self, Balance};
    use sui::sui::SUI;
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;
    use sui::dynamic_field;

    public struct Vehicle has key, store {
        id: UID,
        plate: vector<u8>,
        deck_space: u64,
        owner: address,
    }

    public struct Ferry has key {
        id: UID,
        capacity: u64,
        deck_used: u64,
        toll_per_unit: u64,
        tolls: Balance<SUI>,
        closed: bool,
    }

    public struct PurserCap has key, store {
        id: UID,
    }

    public fun create(
        capacity: u64,
        toll_per_unit: u64,
        ctx: &mut TxContext,
    ): (Ferry, PurserCap) {
        (
            Ferry {
                id: object::new(ctx),
                capacity,
                deck_used: 0,
                toll_per_unit,
                tolls: balance::zero(),
                closed: false,
            },
            PurserCap { id: object::new(ctx) },
        )
    }

    public fun board(
        ferry: &mut Ferry,
        plate: vector<u8>,
        deck_space: u64,
        owner: address,
        toll_payment: Coin<SUI>,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        if (ferry.deck_used + deck_space > ferry.capacity || ferry.closed) {
            return toll_payment;
        };

        ferry.deck_used = ferry.deck_used + deck_space;
        if (ferry.deck_used == ferry.capacity) {
            ferry.closed = true;
        };

        let required = deck_space * ferry.toll_per_unit;
        let toll = coin::take(&mut toll_payment, required, ctx);
        coin::put(&mut ferry.tolls, toll);

        let vehicle = Vehicle {
            id: object::new(ctx),
            plate,
            deck_space,
            owner,
        };
        dynamic_field::add(&mut ferry.id, plate, vehicle);

        toll_payment
    }

    public fun disembark(
        _cap: &PurserCap,
        ferry: &mut Ferry,
        plate: vector<u8>,
    ): Vehicle {
        let vehicle: Vehicle = dynamic_field::remove(&mut ferry.id, plate);
        ferry.deck_used = ferry.deck_used - vehicle.deck_space;
        vehicle
    }

    public fun space_remaining(ferry: &Ferry): u64 {
        ferry.capacity - ferry.deck_used
    }

    public fun tolls_collected(ferry: &Ferry): u64 {
        balance::value(&ferry.tolls)
    }
}
