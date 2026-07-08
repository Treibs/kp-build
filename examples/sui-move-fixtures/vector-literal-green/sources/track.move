module vector_literal_green::track {
    // Edition 2024: vector literals replace the deprecated
    // `vector::empty()` constructor call.
    public fun fresh(): vector<u64> {
        vector[]
    }

    public fun pair(a: u64, b: u64): vector<u64> {
        vector[a, b]
    }
}
