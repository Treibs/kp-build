/// Flash-loan pool for SUI.
///
/// Protocol:
///   1. Anyone may call `borrow` to receive a `Coin<SUI>` plus a hot-potato
///      `Receipt`.
///   2. Because `Receipt` carries no abilities (no copy / drop / store / key),
///      the Move VM refuses to end the transaction while a `Receipt` value still
///      exists on the stack.  The only way to consume it is to pass it to
///      `repay`.
///   3. `repay` verifies that the caller returns at least principal + fee,
///      then deposits the due amount back into the pool and returns any change.
///
/// Fee: 30 basis points (0.30 %), rounded up to the nearest MIST.
module flash_loan::flash_pool {
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin};
    use sui::object::{Self, UID};
    use sui::sui::SUI;
    use sui::transfer;
    use sui::tx_context::TxContext;

    // =========================================================================
    // Constants
    // =========================================================================

    /// 30 bps = 0.30 % flash-loan fee.
    const FEE_BPS: u64 = 30;
    const BPS_DENOM: u64 = 10_000;

    // =========================================================================
    // Error codes
    // =========================================================================

    const EZeroBorrow: u64          = 0;
    const EInsufficientLiquidity: u64 = 1;
    const ERepaymentTooLow: u64     = 2;

    // =========================================================================
    // Structs
    // =========================================================================

    /// Shared pool that holds SUI liquidity.
    public struct FlashPool has key {
        id:          UID,
        reserve:     Balance<SUI>,
        /// Cumulative fee income (informational; updated on each repayment).
        fees_earned: u64,
    }

    /// Hot-potato receipt.
    ///
    /// No abilities → no implicit drop, no copy, cannot be stored.
    /// The VM will abort the transaction unless this value is explicitly
    /// destructured, which only happens inside `repay`.
    public struct Receipt {
        borrow_amount: u64,
        repay_amount:  u64,
    }

    // =========================================================================
    // Pool lifecycle
    // =========================================================================

    /// Create a new `FlashPool` and publish it as a shared object so that any
    /// address can borrow from it within a single programmable transaction block.
    entry fun create_pool(ctx: &mut TxContext) {
        transfer::share_object(FlashPool {
            id:          object::new(ctx),
            reserve:     balance::zero(),
            fees_earned: 0,
        });
    }

    // =========================================================================
    // Liquidity-provider helpers
    // =========================================================================

    /// Deposit SUI into the pool's reserve.
    public fun deposit(pool: &mut FlashPool, payment: Coin<SUI>) {
        balance::join(&mut pool.reserve, coin::into_balance(payment));
    }

    /// Withdraw SUI from the pool's reserve.
    ///
    /// NOTE: in production this should be gated by an admin/LP capability;
    /// it is left open here to keep the example self-contained.
    public fun withdraw(
        pool:   &mut FlashPool,
        amount: u64,
        ctx:    &mut TxContext,
    ): Coin<SUI> {
        coin::take(&mut pool.reserve, amount, ctx)
    }

    // =========================================================================
    // Flash-loan interface
    // =========================================================================

    /// Borrow `amount` MIST from the pool.
    ///
    /// Returns:
    ///   - `Coin<SUI>` — the borrowed funds.
    ///   - `Receipt`   — a hot potato that **must** be passed to `repay` before
    ///                   the transaction ends; it encodes the exact repayment
    ///                   obligation (`principal + fee`).
    public fun borrow(
        pool:   &mut FlashPool,
        amount: u64,
        ctx:    &mut TxContext,
    ): (Coin<SUI>, Receipt) {
        assert!(amount > 0, EZeroBorrow);
        assert!(balance::value(&pool.reserve) >= amount, EInsufficientLiquidity);

        let fee     = fee_for(amount);
        let loan    = coin::take(&mut pool.reserve, amount, ctx);
        let receipt = Receipt { borrow_amount: amount, repay_amount: amount + fee };
        (loan, receipt)
    }

    /// Repay a flash loan.
    ///
    /// `payment` must contain at least `receipt.repay_amount` MIST.
    /// Exactly `repay_amount` is deposited back into the pool; any surplus
    /// is returned to the caller as change.
    ///
    /// Destructuring `receipt` here is the **only** way to satisfy the
    /// hot-potato constraint — enforcing same-transaction repayment at the
    /// type-system level with zero runtime overhead beyond the fee assertion.
    public fun repay(
        pool:    &mut FlashPool,
        receipt: Receipt,
        payment: Coin<SUI>,
        ctx:     &mut TxContext,
    ): Coin<SUI> {
        let Receipt { borrow_amount, repay_amount } = receipt;

        assert!(coin::value(&payment) >= repay_amount, ERepaymentTooLow);

        let mut payment = payment;
        let due         = coin::split(&mut payment, repay_amount, ctx);

        // Track fee income (repay_amount − borrow_amount = fee).
        pool.fees_earned = pool.fees_earned + (repay_amount - borrow_amount);
        balance::join(&mut pool.reserve, coin::into_balance(due));

        // Return change to the caller.
        payment
    }

    // =========================================================================
    // View helpers
    // =========================================================================

    /// Current MIST balance held in the pool's reserve.
    public fun pool_balance(pool: &FlashPool): u64 {
        balance::value(&pool.reserve)
    }

    /// Total fee income collected by the pool since creation.
    public fun fees_earned(pool: &FlashPool): u64 {
        pool.fees_earned
    }

    /// Inspect the repayment obligation recorded in a receipt without
    /// consuming it.  Returns `(borrow_amount, repay_amount)`.
    public fun receipt_amounts(receipt: &Receipt): (u64, u64) {
        (receipt.borrow_amount, receipt.repay_amount)
    }

    // =========================================================================
    // Internal helpers
    // =========================================================================

    /// Compute the flash-loan fee for `amount`, rounded up to the nearest MIST.
    ///
    /// fee = ⌈amount × FEE_BPS / BPS_DENOM⌉
    fun fee_for(amount: u64): u64 {
        (amount * FEE_BPS + BPS_DENOM - 1) / BPS_DENOM
    }
}
