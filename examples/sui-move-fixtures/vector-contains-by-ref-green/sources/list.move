module vector_contains_by_ref_green::list {
    // the element is passed by reference: contains(&v, &e)
    public fun blocked(blocklist: &vector<address>, who: address): bool {
        vector::contains(blocklist, &who)
    }
}
