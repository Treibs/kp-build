module 0x0::show {
    use std::vector;
    use sui::event;

    public struct Firework has store, copy, drop {
        name: vector<u8>,
        burst_size: u64,
    }

    public struct Burst has copy, drop {
        name: vector<u8>,
        size: u64,
    }

    public struct Rack has key, store {
        id: UID,
        fireworks: vector<Firework>,
        show_complete: bool,
    }

    public fun create_rack(ctx: &mut TxContext): Rack {
        Rack {
            id: object::new(ctx),
            fireworks: vector[],
            show_complete: false,
        }
    }

    public fun load_firework(rack: &mut Rack, name: vector<u8>, burst_size: u64) {
        vector::push_back(&mut rack.fireworks, Firework { name, burst_size });
    }

    public fun run_show(rack: &mut Rack) {
        let len = vector::length(&rack.fireworks);
        let mut i = 0;

        while (i < len) {
            let firework = *vector::borrow(&rack.fireworks, i);
            event::emit(Burst { name: firework.name, size: firework.burst_size });
            i = i + 1;
        };

        rack.fireworks = vector[];
        rack.show_complete = true;
    }

    public fun loaded_count(rack: &Rack): u64 {
        vector::length(&rack.fireworks)
    }
}
