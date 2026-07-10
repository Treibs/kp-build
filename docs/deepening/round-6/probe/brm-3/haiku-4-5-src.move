module exam_system::examiner {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};
    use sui::object::{Self, UID, ID};
    use sui::transfer;
    use sui::tx_context::TxContext;
    use sui::table::{Self, Table};

    public struct Certificate has key, store {
        id: UID,
        candidate: address,
        score: u64,
    }

    public struct SubmissionData has store {
        candidate: address,
        score: u64,
        fee: Coin<SUI>,
    }

    public struct Bank has key {
        id: UID,
        balance: Balance<SUI>,
        certificates_issued: u64,
        submissions: Table<ID, SubmissionData>,
    }

    public struct GraderCap has key {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        let bank = Bank {
            id: object::new(ctx),
            balance: balance::zero(),
            certificates_issued: 0,
            submissions: table::new(ctx),
        };
        
        let grader_cap = GraderCap {
            id: object::new(ctx),
        };
        
        transfer::share_object(bank);
        transfer::transfer(grader_cap, ctx.sender());
    }

    public fun submit(
        score: u64,
        payment: Coin<SUI>,
        bank: &mut Bank,
        ctx: &mut TxContext,
    ): ID {
        assert!(score <= 100, 0);
        
        let submission_uid = object::new(ctx);
        let submission_id = object::uid_to_inner(&submission_uid);
        
        let data = SubmissionData {
            candidate: ctx.sender(),
            score,
            fee: payment,
        };
        
        table::add(&mut bank.submissions, submission_id, data);
        object::delete(submission_uid);
        
        submission_id
    }

    public fun grade(
        _cap: &GraderCap,
        bank: &mut Bank,
        submission_id: ID,
        cutoff: u64,
        grading_charge: u64,
        ctx: &mut TxContext,
    ) {
        let SubmissionData { candidate, score, fee } = table::remove(&mut bank.submissions, submission_id);

        if (score >= cutoff) {
            bank.certificates_issued = bank.certificates_issued + 1;
            balance::join(&mut bank.balance, coin::into_balance(fee));
            let certificate = Certificate {
                id: object::new(ctx),
                candidate,
                score,
            };
            transfer::transfer(certificate, candidate);
        } else {
            let charge = coin::split(&mut fee, grading_charge, ctx);
            balance::join(&mut bank.balance, coin::into_balance(charge));
            transfer::public_transfer(fee, candidate);
        };
    }

    public fun certificates_issued(bank: &Bank): u64 {
        bank.certificates_issued
    }

    public fun bank_total(bank: &Bank): u64 {
        balance::value(&bank.balance)
    }
}
