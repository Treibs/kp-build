module gradebook::gradebook {
    use sui::object::UID;
    use sui::table::{Self, Table};
    use sui::event;
    use std::string::String;

    public struct InstructorCap has key, store {
        id: UID,
    }

    public struct GradeBook has key {
        id: UID,
        assignments: vector<Assignment>,
        scores: Table<ScoreKey, u64>,
    }

    public struct Assignment has copy, drop, store {
        name: String,
        max_score: u64,
    }

    public struct ScoreKey has copy, drop, store {
        student: address,
        assignment_idx: u64,
    }

    public struct ScoreAmended has copy, drop {
        student: address,
        assignment_idx: u64,
        old_score: u64,
        new_score: u64,
    }

    public fun create(ctx: &mut TxContext) -> (InstructorCap, GradeBook) {
        let cap = InstructorCap {
            id: object::new(ctx),
        };
        let grade_book = GradeBook {
            id: object::new(ctx),
            assignments: vector[],
            scores: table::new(ctx),
        };
        (cap, grade_book)
    }

    public fun register_assignment(
        _cap: &InstructorCap,
        grade_book: &mut GradeBook,
        name: String,
        max_score: u64,
    ) {
        grade_book.assignments.push_back(Assignment { name, max_score });
    }

    public fun record_score(
        _cap: &InstructorCap,
        grade_book: &mut GradeBook,
        student: address,
        assignment_idx: u64,
        score: u64,
    ) {
        let assignment = &grade_book.assignments[assignment_idx];
        assert!(score <= assignment.max_score);
        
        let key = ScoreKey { student, assignment_idx };
        assert!(!table::contains(&grade_book.scores, key));
        
        table::add(&mut grade_book.scores, key, score);
    }

    public fun amend_score(
        _cap: &InstructorCap,
        grade_book: &mut GradeBook,
        student: address,
        assignment_idx: u64,
        new_score: u64,
    ) {
        let key = ScoreKey { student, assignment_idx };
        assert!(table::contains(&grade_book.scores, key));
        
        let assignment = &grade_book.assignments[assignment_idx];
        assert!(new_score <= assignment.max_score);
        
        let old_score = *table::borrow(&grade_book.scores, key);
        *table::borrow_mut(&mut grade_book.scores, key) = new_score;
        
        event::emit(ScoreAmended {
            student,
            assignment_idx,
            old_score,
            new_score,
        });
    }

    public fun student_total(grade_book: &GradeBook, student: address): u64 {
        let mut total = 0;
        let mut i = 0;
        let len = grade_book.assignments.length();
        
        while (i < len) {
            let key = ScoreKey { student, assignment_idx: i };
            if (table::contains(&grade_book.scores, key)) {
                total = total + *table::borrow(&grade_book.scores, key);
            };
            i = i + 1;
        };
        
        total
    }

    public fun has_score(grade_book: &GradeBook, student: address, assignment_idx: u64): bool {
        let key = ScoreKey { student, assignment_idx };
        table::contains(&grade_book.scores, key)
    }
}
