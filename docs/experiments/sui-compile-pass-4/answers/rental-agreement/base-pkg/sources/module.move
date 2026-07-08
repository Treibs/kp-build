module rental::rental {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;

    public struct RentalAgreement<T: key + store> has key, store {
        id: UID,
        owner: address,
        renter: address,
        item: T,
        deposit: Coin<SUI>,
        rent: Coin<SUI>,
        per_epoch_price: u64,
        epochs_rented: u64,
        epochs_elapsed: u64,
    }

    public fun create_rental<T: key + store>(
        item: T,
        owner: address,
        per_epoch_price: u64,
        deposit: Coin<SUI>,
        rent: Coin<SUI>,
        epochs_to_rent: u64,
        renter: address,
        ctx: &mut TxContext,
    ): RentalAgreement<T> {
        assert!(coin::value(&rent) == per_epoch_price * epochs_to_rent, 0);

        RentalAgreement {
            id: object::new(ctx),
            owner,
            renter,
            item,
            deposit,
            rent,
            per_epoch_price,
            epochs_rented: epochs_to_rent,
            epochs_elapsed: 0,
        }
    }

    public fun return_on_time<T: key + store>(
        agreement: RentalAgreement<T>,
        ctx: &mut TxContext,
    ): T {
        assert!(tx_context::sender(ctx) == agreement.renter, 1);
        assert!(agreement.epochs_elapsed < agreement.epochs_rented, 2);

        let RentalAgreement {
            id,
            owner,
            renter,
            item,
            deposit,
            rent,
            per_epoch_price: _,
            epochs_rented: _,
            epochs_elapsed: _,
        } = agreement;

        transfer::public_transfer(deposit, renter);
        transfer::public_transfer(rent, owner);
        object::delete(id);
        
        item
    }

    public fun reclaim_after_expiry<T: key + store>(
        agreement: RentalAgreement<T>,
        ctx: &mut TxContext,
    ): T {
        assert!(tx_context::sender(ctx) == agreement.owner, 3);
        assert!(agreement.epochs_elapsed >= agreement.epochs_rented, 4);

        let RentalAgreement {
            id,
            owner,
            renter: _,
            item,
            deposit,
            rent,
            per_epoch_price: _,
            epochs_rented: _,
            epochs_elapsed: _,
        } = agreement;

        transfer::public_transfer(deposit, owner);
        transfer::public_transfer(rent, owner);
        object::delete(id);
        
        item
    }

    public fun advance_epoch<T: key + store>(
        agreement: &mut RentalAgreement<T>,
    ) {
        agreement.epochs_elapsed = agreement.epochs_elapsed + 1;
    }
}
