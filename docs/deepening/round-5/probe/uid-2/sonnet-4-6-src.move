module museum::desk {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};
    use sui::table::{Self, Table};
    use std::string::String;

    public struct MuseumCap has key, store {
        id: UID,
    }

    public struct Artifact has key, store {
        id: UID,
        name: String,
    }

    public struct LoanRecord has store {
        borrower: address,
        due_ms: u64,
        deposit: u64,
    }

    public struct LoanDesk has key {
        id: UID,
        museum: address,
        register: Table<ID, LoanRecord>,
        pool: Balance<SUI>,
    }

    fun init(ctx: &mut TxContext) {
        transfer::transfer(MuseumCap { id: object::new(ctx) }, ctx.sender());
        transfer::share_object(LoanDesk {
            id: object::new(ctx),
            museum: ctx.sender(),
            register: table::new(ctx),
            pool: balance::zero(),
        });
    }

    public fun create_artifact(
        _cap: &MuseumCap,
        name: String,
        ctx: &mut TxContext,
    ): Artifact {
        Artifact { id: object::new(ctx), name }
    }

    /// Museum (MuseumCap holder) initiates the loan, transferring the artifact to
    /// the borrower. The deposit coin — sourced from the borrower in the same PTB —
    /// is absorbed into the desk pool.
    public fun loan_artifact(
        desk: &mut LoanDesk,
        _cap: &MuseumCap,
        artifact: Artifact,
        borrower: address,
        due_ms: u64,
        deposit: Coin<SUI>,
    ) {
        let artifact_id = object::id(&artifact);
        let deposit_amount = coin::value(&deposit);
        balance::join(&mut desk.pool, coin::into_balance(deposit));
        table::add(&mut desk.register, artifact_id, LoanRecord {
            borrower,
            due_ms,
            deposit: deposit_amount,
        });
        transfer::public_transfer(artifact, borrower);
    }

    /// Borrower returns the artifact, closing its register entry and receiving the
    /// full deposit back. The artifact is forwarded to the museum address recorded
    /// at desk creation.
    public fun return_artifact(
        desk: &mut LoanDesk,
        artifact: Artifact,
        ctx: &mut TxContext,
    ) {
        let artifact_id = object::id(&artifact);
        let LoanRecord { borrower, due_ms: _, deposit } =
            table::remove(&mut desk.register, artifact_id);
        assert!(ctx.sender() == borrower);
        let refund = coin::from_balance(balance::split(&mut desk.pool, deposit), ctx);
        transfer::public_transfer(refund, borrower);
        let museum = desk.museum;
        transfer::public_transfer(artifact, museum);
    }
}
