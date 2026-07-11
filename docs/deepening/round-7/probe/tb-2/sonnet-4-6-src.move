module seed_vault::vault {
    use std::option::{Self, Option};

    public struct LabCap has key, store {
        id: UID,
    }

    public struct Reading has copy, drop, store {
        year: u64,
        rate: u64,
    }

    public struct Sample has key {
        id: UID,
        readings: vector<Reading>,
    }

    fun init(ctx: &mut TxContext) {
        transfer::transfer(LabCap { id: object::new(ctx) }, ctx.sender());
    }

    public fun create_sample(ctx: &mut TxContext) {
        transfer::share_object(Sample {
            id: object::new(ctx),
            readings: vector[],
        });
    }

    public fun append_reading(_cap: &LabCap, sample: &mut Sample, year: u64, rate: u64) {
        vector::push_back(&mut sample.readings, Reading { year, rate });
    }

    public fun reading_count(sample: &Sample): u64 {
        vector::length(&sample.readings)
    }

    public fun best_reading(sample: &Sample): Option<Reading> {
        let len = vector::length(&sample.readings);
        if (len == 0) {
            return option::none()
        };
        let mut best = *vector::borrow(&sample.readings, 0);
        let mut i = 1u64;
        while (i < len) {
            let r = *vector::borrow(&sample.readings, i);
            if (r.rate > best.rate) {
                best = r;
            };
            i = i + 1;
        };
        option::some(best)
    }

    public fun reading_year(r: &Reading): u64 { r.year }
    public fun reading_rate(r: &Reading): u64 { r.rate }
}
