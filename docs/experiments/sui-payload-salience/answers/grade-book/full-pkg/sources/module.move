module gradebook::gradebook {
    use sui::table::{Self, Table};
    use sui::event;

    public struct GradeBook has key, store {
        id: UID,
        assignments: vector<Assignment>,
        scores: Table<(address, u64), u64>,
    }

    public struct Assignment has drop, store {
        name: vector<u8>,
        max_score: u64,
    }

    public struct InstructorCap has key, store {
        id: UID,
    }

    public struct ScoreAmended has copy, drop {
        student: address,
        assignment_index: u64,
        old_score: u64,
        new_score: u64,
    }

    public fun create_gradebook(ctx: &mut TxContext): InstructorCap {
        let gradebook = GradeBook {
            id: object::new(ctx),
            assignments: vector[],
            scores: table::new(ctx),
        };
        transfer::share_object(gradebook);
        
        InstructorCap {
            id: object::new(ctx),
        }
    }

    public fun register_assignment(
        gradebook: &mut GradeBook,
        _cap: &InstructorCap,
        name: vector<u8>,
        max_score: u64,
    ) {
        gradebook.assignments.push_back(Assignment { name, max_score });
    }

    public fun record_score(
        gradebook: &mut GradeBook,
        _cap: &InstructorCap,
        student: address,
        assignment_index: u64,
        score: u64,
    ) {
        let assignment = &gradebook.assignments[assignment_index];
        assert!(score <= assignment.max_score, 0);
        
        let key = (student, assignment_index);
        assert!(!table::contains(&gradebook.scores, key), 1);
        
        table::add(&mut gradebook.scores, key, score);
    }

    public fun amend_score(
        gradebook: &mut GradeBook,
        _cap: &InstructorCap,
        student: address,
        assignment_index: u64,
        new_score: u64,
    ) {
        let assignment = &gradebook.assignments[assignment_index];
        assert!(new_score <= assignment.max_score, 2);
        
        let key = (student, assignment_index);
        assert!(table::contains(&gradebook.scores, key), 3);
        
        let old_score = table::remove(&mut gradebook.scores, key);
        table::add(&mut gradebook.scores, key, new_score);
        
        event::emit(ScoreAmended {
            student,
            assignment_index,
            old_score,
            new_score,
        });
    }

    public fun student_total(
        gradebook: &GradeBook,
        student: address,
    ): u64 {
        let mut total = 0u64;
        let mut i = 0u64;
        while (i < gradebook.assignments.length()) {
            let key = (student, i);
            if (table::contains(&gradebook.scores, key)) {
                total = total + *table::borrow(&gradebook.scores, key);
            };
            i = i + 1;
        };
        total
    }

    public fun has_score(
        gradebook: &GradeBook,
        student: address,
        assignment_index: u64,
    ): bool {
        let key = (student, assignment_index);
        table::contains(&gradebook.scores, key)
    }
}
