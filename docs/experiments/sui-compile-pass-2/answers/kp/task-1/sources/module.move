/// Flash-loan pool for native SUI.
///
/// `borrow` issues a `Coin<SUI>` together with a `FlashLoanReceipt` hot potato.
/// Because the receipt declares **no abilities** the Move VM will abort the
/// transaction if it is not passed to `repay` before the transaction ends,
/// guaranteeing that every borrow is repaid (principal + fee) in the same PTB.
module flash_loan::pool {
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::event;
    use sui::object::ID;
    use sui::sui::SUI;

    // ── error codes ──────────────────────────────────────────────────────────

    /// Pool does not hold enough SUI to satisfy the request.
    const EInsufficientPoolBalance: u64 = 0;
    /// Repayment coin does not cover principal + fee.
    const EInsufficientRepayment: u64 = 1;
    /// Receipt was issued for a different pool.
    const EPoolMismatch: u64 = 2;

    // ── objects ──────────────────────────────────────────────────────────────

    /// Grants the right to withdraw liquidity and adjust the fee.
    public struct AdminCap has key, store {
        id: UID,
    }

    /// Shared liquidity pool that backs the flash loans.
    public struct Pool has key {
        id: UID,
        balance: Balance<SUI>,
        /// Fee denominated in basis points (1 bps = 0.01 %).  Default: 30 bps = 0.30 %.
        fee_bps: u64,
    }

    // ── hot potato ───────────────────────────────────────────────────────────

    /// Proof-of-borrow returned alongside the borrowed `Coin<SUI>`.
    ///
    /// This struct intentionally declares **no abilities**.  The Move VM
    /// requires every non-drop value to be consumed before a transaction
    /// commits.  A caller who fails to pass this to `repay` will cause the
    /// entire transaction to abort, reverting all state changes.
    public struct FlashLoanReceipt {
        pool_id: ID,
        borrowed_amount: u64,
    }

    // ── events ───────────────────────────────────────────────────────────────

    public struct Borrowed has copy, drop {
        pool_id: ID,
        borrower: address,
        amount: u64,
        fee: u64,
    }

    public struct Repaid has copy, drop {
        pool_id: ID,
        amount: u64,
        fee: u64,
    }

    // ── initialiser ──────────────────────────────────────────────────────────

    fun init(ctx: &mut TxContext) {
        // Transfer the admin capability to the deployer.
        transfer::transfer(
            AdminCap { id: object::new(ctx) },
            ctx.sender(),
        );
        // Publish the pool as a shared object so anyone can interact with it.
        transfer::share_object(Pool {
            id: object::new(ctx),
            balance: balance::zero<SUI>(),
            fee_bps: 30,
        });
    }

    // ── liquidity management ─────────────────────────────────────────────────

    /// Add SUI to the pool.  Open to anyone.
    public fun deposit(pool: &mut Pool, coin: Coin<SUI>) {
        pool.balance.join(coin.into_balance());
    }

    /// Remove `amount` MIST from the pool.  Requires the `AdminCap`.
    public fun withdraw(
        _cap: &AdminCap,
        pool: &mut Pool,
        amount: u64,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        coin::from_balance(pool.balance.split(amount), ctx)
    }

    /// Update the fee rate.  Requires the `AdminCap`.
    public fun set_fee_bps(
        _cap: &AdminCap,
        pool: &mut Pool,
        new_fee_bps: u64,
    ) {
        pool.fee_bps = new_fee_bps;
    }

    // ── flash loan ───────────────────────────────────────────────────────────

    /// Borrow `amount` MIST from the pool in a single programmable transaction.
    ///
    /// Returns:
    ///   1. A `Coin<SUI>` containing the borrowed funds.
    ///   2. A `FlashLoanReceipt` hot potato that **must** be consumed by `repay`
    ///      in the same transaction.  Failing to call `repay` aborts the
    ///      transaction and reverts every state change, including the borrow.
    public fun borrow(
        pool: &mut Pool,
        amount: u64,
        ctx: &mut TxContext,
    ): (Coin<SUI>, FlashLoanReceipt) {
        assert!(pool.balance.value() >= amount, EInsufficientPoolBalance);

        let pool_id = object::id(pool);
        let fee = compute_fee(amount, pool.fee_bps);

        event::emit(Borrowed {
            pool_id,
            borrower: ctx.sender(),
            amount,
            fee,
        });

        (
            coin::from_balance(pool.balance.split(amount), ctx),
            FlashLoanReceipt { pool_id, borrowed_amount: amount },
        )
    }

    /// Repay the flash loan and satisfy the hot-potato constraint.
    ///
    /// `payment` must contain at least `borrowed_amount + fee` MIST.
    /// Any excess above that is returned to the caller as a separate coin
    /// (which may be zero-value and should be destroyed with `coin::destroy_zero`).
    ///
    /// The `receipt` is consumed here by destructuring — the only valid way to
    /// dispose of a no-abilities struct without aborting the transaction.
    public fun repay(
        pool: &mut Pool,
        payment: Coin<SUI>,
        receipt: FlashLoanReceipt,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        // Destructure the hot potato.  This is the sole valid disposal path.
        let FlashLoanReceipt { pool_id, borrowed_amount } = receipt;

        assert!(pool_id == object::id(pool), EPoolMismatch);

        let fee = compute_fee(borrowed_amount, pool.fee_bps);
        let required = borrowed_amount + fee;
        assert!(payment.value() >= required, EInsufficientRepayment);

        event::emit(Repaid { pool_id, amount: borrowed_amount, fee });

        // Rebind as mutable to allow `split`, then return the excess.
        let mut payment = payment;
        let repayment = payment.split(required, ctx);
        pool.balance.join(repayment.into_balance());

        payment // excess (possibly zero-value)
    }

    // ── view helpers ─────────────────────────────────────────────────────────

    /// Current pool balance in MIST.
    public fun pool_balance(pool: &Pool): u64 {
        pool.balance.value()
    }

    /// Current fee rate in basis points.
    public fun fee_bps(pool: &Pool): u64 {
        pool.fee_bps
    }

    // ── internal ─────────────────────────────────────────────────────────────

    fun compute_fee(amount: u64, fee_bps: u64): u64 {
        (amount * fee_bps) / 10000
    }

    // ── tests ─────────────────────────────────────────────────────────────────

    #[test_only]
    use sui::test_scenario;

    #[test]
    fun test_borrow_and_repay() {
        let admin = @0xAD;
        let borrower = @0xB0;

        let mut scenario = test_scenario::begin(admin);

        // tx 0 — run the module initialiser
        {
            init(scenario.ctx());
        };

        // tx 1 — seed the pool with 1 SUI (= 1_000_000_000 MIST)
        scenario.next_tx(admin);
        {
            let mut pool = scenario.take_shared<Pool>();
            let seed = coin::mint_for_testing<SUI>(1_000_000_000, scenario.ctx());
            deposit(&mut pool, seed);
            test_scenario::return_shared(pool);
        };

        // tx 2 — flash-loan round trip inside a single PTB
        scenario.next_tx(borrower);
        {
            let mut pool = scenario.take_shared<Pool>();
            let balance_before = pool_balance(&pool);
            let borrow_amt = 500_000u64;

            // borrow: pool shrinks by exactly borrow_amt
            let (borrowed, receipt) = borrow(&mut pool, borrow_amt, scenario.ctx());
            assert!(pool_balance(&pool) == balance_before - borrow_amt, 10);

            // build repayment = principal + fee
            let fee = compute_fee(borrow_amt, pool.fee_bps);
            let fee_coin = coin::mint_for_testing<SUI>(fee, scenario.ctx());
            let mut repayment = borrowed;
            repayment.join(fee_coin);

            // repay: pool grows by fee; no excess
            let excess = repay(&mut pool, repayment, receipt, scenario.ctx());
            assert!(pool_balance(&pool) == balance_before + fee, 20);
            assert!(excess.value() == 0, 30);
            excess.destroy_zero();

            test_scenario::return_shared(pool);
        };

        scenario.end();
    }

    #[test]
    #[expected_failure(abort_code = EInsufficientPoolBalance)]
    fun test_borrow_exceeds_balance_aborts() {
        let admin = @0xAD;
        let mut scenario = test_scenario::begin(admin);

        {
            init(scenario.ctx());
        };

        scenario.next_tx(admin);
        {
            let mut pool = scenario.take_shared<Pool>();
            // Pool is empty; any borrow should abort.
            let (_coin, _receipt) = borrow(&mut pool, 1, scenario.ctx());
            // unreachable — abort expected above
            test_scenario::return_shared(pool);
        };

        scenario.end();
    }

    #[test]
    #[expected_failure(abort_code = EInsufficientRepayment)]
    fun test_underpayment_aborts() {
        let admin = @0xAD;
        let mut scenario = test_scenario::begin(admin);

        {
            init(scenario.ctx());
        };

        scenario.next_tx(admin);
        {
            let mut pool = scenario.take_shared<Pool>();
            let seed = coin::mint_for_testing<SUI>(1_000_000_000, scenario.ctx());
            deposit(&mut pool, seed);
            test_scenario::return_shared(pool);
        };

        scenario.next_tx(admin);
        {
            let mut pool = scenario.take_shared<Pool>();
            let borrow_amt = 100_000u64;
            let (borrowed, receipt) = borrow(&mut pool, borrow_amt, scenario.ctx());

            // Repay with principal only — fee is missing, must abort.
            let excess = repay(&mut pool, borrowed, receipt, scenario.ctx());
            excess.destroy_zero();

            test_scenario::return_shared(pool);
        };

        scenario.end();
    }
}
