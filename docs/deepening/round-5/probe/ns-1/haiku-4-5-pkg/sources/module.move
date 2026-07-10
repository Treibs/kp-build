module attendance::sheet {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::TxContext;
    use sui::table::{Self, Table};

    public struct AttendanceSheet has key {
        id: UID,
        attendance: Table<address, u64>,
        total_students: u64,
    }

    public struct TeacherCap has key, store {
        id: UID,
    }

    public struct SHEET has drop {}

    fun init(witness: SHEET, ctx: &mut TxContext) {
        let sheet = AttendanceSheet {
            id: object::new(ctx),
            attendance: table::new(ctx),
            total_students: 0,
        };

        let cap = TeacherCap {
            id: object::new(ctx),
        };

        transfer::share_object(sheet);
        transfer::transfer(cap, ctx.sender());
    }

    public fun mark_present(sheet: &mut AttendanceSheet, student: address, _cap: &TeacherCap) {
        if (!table::contains(&sheet.attendance, student)) {
            table::add(&mut sheet.attendance, student, 1);
            sheet.total_students = sheet.total_students + 1;
        } else {
            let current = table::borrow_mut(&mut sheet.attendance, student);
            *current = *current + 1;
        };
    }

    public fun get_attendance(sheet: &AttendanceSheet, student: address): u64 {
        if (table::contains(&sheet.attendance, student)) {
            *table::borrow(&sheet.attendance, student)
        } else {
            0
        }
    }

    public fun get_total_students(sheet: &AttendanceSheet): u64 {
        sheet.total_students
    }
}
