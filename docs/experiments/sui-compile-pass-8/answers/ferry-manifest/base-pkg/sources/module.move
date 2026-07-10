module ferry::manifest {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::transfer;
    use sui::object::{Self, UID};
    use sui::tx_context::{Self, TxContext};

    public struct Ferry has key {
        id: UID,
        capacity: u64,
        space_used: u64,
        toll_rate: u64,
        tolls_collected: u64,
        is_closed: bool,
    }

    public struct Vehicle has key, store {
        id: UID,
        plate: vector<u8>,
        deck_space: u64,
        owner: address,
    }

    public struct PurserCap has key {
        id: UID,
    }

    public fun new(
        capacity: u64,
        toll_rate: u64,
        ctx: &mut TxContext
    ): (Ferry, PurserCap) {
        (
            Ferry {
                id: object::new(ctx),
                capacity,
                space_used: 0,
                toll_rate,
                tolls_collected: 0,
                is_closed: false,
            },
            PurserCap { id: object::new(ctx) }
        )
    }

    public fun board(
        ferry: &mut Ferry,
        plate: vector<u8>,
        deck_space: u64,
        owner: address,
        payment: Coin<SUI>,
        ctx: &mut TxContext
    ): Option<Vehicle> {
        if (ferry.is_closed) {
            transfer::public_transfer(payment, tx_context::sender(ctx));
            return std::option::none()
        }

        if (ferry.space_used + deck_space > ferry.capacity) {
            transfer::public_transfer(payment, tx_context::sender(ctx));
            return std::option::none()
        }

        let required_toll = deck_space * ferry.toll_rate;
        let paid = coin::value(&payment);

        if (paid < required_toll) {
            transfer::public_transfer(payment, tx_context::sender(ctx));
            return std::option::none()
        }

        ferry.space_used = ferry.space_used + deck_space;
        ferry.tolls_collected = ferry.tolls_collected + required_toll;

        if (ferry.space_used == ferry.capacity) {
            ferry.is_closed = true;
        }

        if (paid > required_toll) {
            let change = coin::take(&mut payment, paid - required_toll, ctx);
            transfer::public_transfer(change, tx_context::sender(ctx));
        }

        coin::burn_for_free(payment);

        std::option::some(Vehicle {
            id: object::new(ctx),
            plate,
            deck_space,
            owner,
        })
    }

    public fun disembark(
        _cap: &PurserCap,
        vehicle: Vehicle,
    ) {
        transfer::public_transfer(vehicle, vehicle.owner);
    }

    public fun space_remaining(ferry: &Ferry): u64 {
        ferry.capacity - ferry.space_used
    }

    public fun tolls_collected(ferry: &Ferry): u64 {
        ferry.tolls_collected
    }
}
