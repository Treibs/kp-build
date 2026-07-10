module @0x1::grading {
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;
    use sui::transfer;
    use sui::event;
    use sui::balance::{Self, Balance};
    use sui::sui::SUI;
    use sui::coin::{Self, Coin};
    use sui::table::{Self, Table};

    const SCORE_TOO_HIGH: u64 = 1;
    const SUBMISSION_NOT_FOUND: u64 = 2;

    public struct GraderCap has key, store {
        id: UID,
    }

    public struct Certificate has key, store {
        id: UID,
        candidate: address,
        score: u64,
    }

    public struct Submission has copy, drop {
        candidate: address,
        score: u64,
        fee: u64,
    }

    public struct ExamBank has key {
        id: UID,
        total_banked: Balance<SUI>,
        grading_charge: u64,
        score_cutoff: u64,
        submissions: Table<address, Submission>,
        certificates_issued: u64,
    }

    public struct SubmissionReceived has copy, drop {
        candidate: address,
        score: u64,
        fee: u64,
    }

    public struct GradingCompleted has copy, drop {
        candidate: address,
        score: u64,
        passed: bool,
    }

    fun init(ctx: &mut TxContext) {
        let grader_cap = GraderCap {
            id: object::new(ctx),
        };

        let bank = ExamBank {
            id: object::new(ctx),
            total_banked: balance::zero(),
            grading_charge: 100,
            score_cutoff: 70,
            submissions: table::new(ctx),
            certificates_issued: 0,
        };

        transfer::transfer(grader_cap, ctx.sender());
        transfer::share_object(bank);
    }

    public fun submit_score(
        bank: &mut ExamBank,
        score: u64,
        payment: Coin<SUI>,
        ctx: &mut TxContext,
    ) {
        assert!(score <= 100, SCORE_TOO_HIGH);

        let submission = Submission {
            candidate: ctx.sender(),
            score,
            fee: payment.value(),
        };

        table::add(&mut bank.submissions, ctx.sender(), submission);

        event::emit(SubmissionReceived {
            candidate: ctx.sender(),
            score,
            fee: payment.value(),
        });

        balance::join(&mut bank.total_banked, coin::into_balance(payment));
    }

    public fun grade_submission(
        bank: &mut ExamBank,
        candidate: address,
        _cap: &GraderCap,
        ctx: &mut TxContext,
    ) {
        assert!(table::contains(&bank.submissions, candidate), SUBMISSION_NOT_FOUND);

        let submission = table::remove(&mut bank.submissions, candidate);
        let passed = submission.score >= bank.score_cutoff;

        if (passed) {
            let cert = Certificate {
                id: object::new(ctx),
                candidate,
                score: submission.score,
            };

            bank.certificates_issued = bank.certificates_issued + 1;

            transfer::transfer(cert, candidate);

            event::emit(GradingCompleted {
                candidate,
                score: submission.score,
                passed: true,
            });
        } else {
            let refund_amount = submission.fee - bank.grading_charge;
            if (refund_amount > 0) {
                let refund_balance = balance::split(&mut bank.total_banked, refund_amount);
                let refund = coin::from_balance(refund_balance);
                transfer::public_transfer(refund, candidate);
            };

            event::emit(GradingCompleted {
                candidate,
                score: submission.score,
                passed: false,
            });
        };
    }

    public fun bank_total(bank: &ExamBank): u64 {
        balance::value(&bank.total_banked)
    }

    public fun certificates_issued(bank: &ExamBank): u64 {
        bank.certificates_issued
    }
}
