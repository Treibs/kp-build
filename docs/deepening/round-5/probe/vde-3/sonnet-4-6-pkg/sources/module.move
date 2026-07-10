module fireworks::show {
    use std::string::String;
    use sui::event;

    public struct Firework has store, drop {
        name: String,
        burst_size: u64,
    }

    public struct Rack has key {
        id: UID,
        fireworks: vector<Firework>,
        complete: bool,
    }

    public struct Burst has copy, drop {
        name: String,
        size: u64,
    }

    public fun new_rack(ctx: &mut TxContext) {
        transfer::share_object(Rack {
            id: object::new(ctx),
            fireworks: vector[],
            complete: false,
        });
    }

    public fun load(rack: &mut Rack, name: String, burst_size: u64) {
        assert!(!rack.complete);
        rack.fireworks.push_back(Firework { name, burst_size });
    }

    public fun run_show(rack: &mut Rack) {
        assert!(!rack.complete);
        rack.fireworks.reverse();
        while (!rack.fireworks.is_empty()) {
            let Firework { name, burst_size } = rack.fireworks.pop_back();
            event::emit(Burst { name, size: burst_size });
        };
        rack.complete = true;
    }

    public fun firework_count(rack: &Rack): u64 {
        rack.fireworks.length()
    }
}
