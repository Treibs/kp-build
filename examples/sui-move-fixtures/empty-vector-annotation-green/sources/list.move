module empty_vector_annotation_green::list {
    // an empty vector with no later type evidence needs its element
    // type stated at creation — the typed literal form
    public fun fresh_count(): u64 {
        let owners = vector<address>[];
        vector::length(&owners)
    }
}
