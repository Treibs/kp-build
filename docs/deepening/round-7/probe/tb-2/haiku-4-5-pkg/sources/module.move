module seed_vault::vault {
    use std::vector;
    use std::option::{Self, Option};

    public struct Sample has key {
        id: UID,
        readings: vector<Reading>,
    }

    public struct Reading has copy, drop, store {
        year: u64,
        rate: u64,
    }

    public struct LabCap has key, store {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        let cap = LabCap {
            id: object::new(ctx),
        };
        transfer::transfer(cap, ctx.sender());
    }

    public fun create_sample(ctx: &mut TxContext): Sample {
        Sample {
            id: object::new(ctx),
            readings: vector[],
        }
    }

    public fun append_reading(
        sample: &mut Sample,
        year: u64,
        rate: u64,
        _cap: &LabCap,
    ) {
        vector::push_back(&mut sample.readings, Reading { year, rate });
    }

    public fun best_reading(sample: &Sample): Option<(u64, u64)> {
        let len = vector::length(&sample.readings);
        if (len == 0) {
            return option::none()
        };

        let mut best_year = 0;
        let mut best_rate = 0;
        let mut i = 0;

        while (i < len) {
            let reading = vector::borrow(&sample.readings, i);
            if (i == 0 || reading.rate > best_rate) {
                best_year = reading.year;
                best_rate = reading.rate;
            };
            i = i + 1;
        };

        option::some((best_year, best_rate))
    }

    public fun reading_count(sample: &Sample): u64 {
        vector::length(&sample.readings)
    }
}
