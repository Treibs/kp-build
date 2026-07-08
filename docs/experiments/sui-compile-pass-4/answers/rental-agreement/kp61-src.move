module rental::agreement {
    use sui::coin::Coin;
    use sui::sui::SUI;
    use sui::clock::Clock;
    use sui::transfer;
    use sui::option;

    public struct RentalAgreement<T: key + store> has key, store {
        id: UID,
        item: T,
        owner: address,
        renter: address,
        deposit: option::Option<Coin<SUI>>,
        rent_paid: option::Option<Coin<SUI>>,
        per_epoch_price: u64,
        required_deposit: u64,
        epochs_rented: u64,
        rental_started_at: u64,
    }

    public fun create_listing<T: key + store>(
        item: T,
        per_epoch_price: u64,
        required_deposit: u64,
        ctx: &mut TxContext,
    ) {
        let agreement = RentalAgreement {
            id: object::new(ctx),
            item,
            owner: ctx.sender(),
            renter: @0x0,
            deposit: option::none(),
            rent_paid: option::none(),
            per_epoch_price,
            required_deposit,
            epochs_rented: 0,
            rental_started_at: 0,
        };
        transfer::share_object(agreement);
    }

    public fun take_rental<T: key + store>(
        agreement: &mut RentalAgreement<T>,
        deposit: Coin<SUI>,
        rent: Coin<SUI>,
        epochs: u64,
        clock: &Clock,
        ctx: &mut TxContext,
    ) {
        assert!(deposit.value() >= agreement.required_deposit, "Deposit insufficient");
        assert!(rent.value() == agreement.per_epoch_price * epochs, "Rent amount mismatch");
        assert!(agreement.renter == @0x0, "Already rented");

        agreement.renter = ctx.sender();
        agreement.epochs_rented = epochs;
        agreement.rental_started_at = clock.timestamp_ms() / 1000;
        agreement.deposit = option::some(deposit);
        agreement.rent_paid = option::some(rent);
    }

    public fun return_item<T: key + store>(
        mut agreement: RentalAgreement<T>,
        clock: &Clock,
        ctx: &mut TxContext,
    ): T {
        let current_time = clock.timestamp_ms() / 1000;
        let rental_end = agreement.rental_started_at + agreement.epochs_rented;

        assert!(current_time <= rental_end, "Rental period expired");
        assert!(ctx.sender() == agreement.renter, "Not the renter");

        let item = agreement.item;
        let deposit = option::extract(&mut agreement.deposit);
        let rent = option::extract(&mut agreement.rent_paid);

        transfer::public_transfer(deposit, agreement.renter);
        transfer::public_transfer(rent, agreement.owner);

        let RentalAgreement {
            id,
            item: _,
            owner: _,
            renter: _,
            deposit: _,
            rent_paid: _,
            per_epoch_price: _,
            required_deposit: _,
            epochs_rented: _,
            rental_started_at: _,
        } = agreement;

        object::delete(id);
        item
    }

    public fun reclaim_item<T: key + store>(
        mut agreement: RentalAgreement<T>,
        clock: &Clock,
        ctx: &mut TxContext,
    ): T {
        let current_time = clock.timestamp_ms() / 1000;
        let rental_end = agreement.rental_started_at + agreement.epochs_rented;

        assert!(current_time > rental_end, "Rental period not expired");
        assert!(ctx.sender() == agreement.owner, "Not the owner");

        let item = agreement.item;
        let deposit = option::extract(&mut agreement.deposit);
        let rent = option::extract(&mut agreement.rent_paid);

        transfer::public_transfer(deposit, agreement.owner);
        transfer::public_transfer(rent, agreement.owner);

        let RentalAgreement {
            id,
            item: _,
            owner: _,
            renter: _,
            deposit: _,
            rent_paid: _,
            per_epoch_price: _,
            required_deposit: _,
            epochs_rented: _,
            rental_started_at: _,
        } = agreement;

        object::delete(id);
        item
    }
}
