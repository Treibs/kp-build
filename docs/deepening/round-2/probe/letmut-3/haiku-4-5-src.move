module dedup::dedup {
    public fun unique(addrs: vector<address>): vector<address> {
        let mut result = std::vector::empty<address>();
        let len = std::vector::length(&addrs);
        let mut i = 0;
        
        while (i < len) {
            let addr = *std::vector::borrow(&addrs, i);
            if (!std::vector::contains(&result, &addr)) {
                std::vector::push_back(&mut result, addr);
            }
            i = i + 1;
        }
        
        result
    }
}
