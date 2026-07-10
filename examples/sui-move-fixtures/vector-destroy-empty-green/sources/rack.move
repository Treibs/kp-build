module vector_destroy_empty_green::rack {
    public struct Rocket has key, store {
        id: UID,
    }

    // a drained vector of non-drop elements is consumed explicitly
    public fun launch_all(mut rockets: vector<Rocket>, pad: address) {
        while (!vector::is_empty(&rockets)) {
            let r = vector::pop_back(&mut rockets);
            transfer::public_transfer(r, pad);
        };
        vector::destroy_empty(rockets);
    }
}
