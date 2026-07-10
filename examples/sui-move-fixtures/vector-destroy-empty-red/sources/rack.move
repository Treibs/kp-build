module vector_destroy_empty_red::rack {
    public struct Rocket has key, store {
        id: UID,
    }

    // drained to empty, but vector<Rocket> still lacks drop at the brace —
    // the emptied vector must be destroy_empty'd (see green)
    public fun launch_all(mut rockets: vector<Rocket>, pad: address) {
        while (!vector::is_empty(&rockets)) {
            let r = vector::pop_back(&mut rockets);
            transfer::public_transfer(r, pad);
        };
    }
}
