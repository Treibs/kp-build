module vector_contains_by_ref_red::list {
    // vector::contains takes the probe element BY REFERENCE
    public fun blocked(blocklist: &vector<address>, who: address): bool {
        vector::contains(blocklist, who)
    }
}
