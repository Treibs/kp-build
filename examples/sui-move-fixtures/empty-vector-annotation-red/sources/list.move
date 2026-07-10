module empty_vector_annotation_red::list {
    // vector::empty() with no annotation and no downstream element
    // evidence cannot be inferred
    public fun fresh_count(): u64 {
        let owners = vector::empty();
        vector::length(&owners)
    }
}
