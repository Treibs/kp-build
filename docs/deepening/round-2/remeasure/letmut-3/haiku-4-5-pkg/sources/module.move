module dedup::dedup {
    use std::vector;

    public fun unique(addrs: vector<address>): vector<address> {
        let mut result = vector[];
        let mut i = 0;
        
        while (i < vector::length(&addrs)) {
            let addr = *vector::borrow(&addrs, i);
            let mut found = false;
            let mut j = 0;
            
            while (j < vector::length(&result)) {
                if (*vector::borrow(&result, j) == addr) {
                    found = true;
                    break;
                };
                j = j + 1;
            };
            
            if (!found) {
                vector::push_back(&mut result, addr);
            };
            
            i = i + 1;
        };
        
        result
    }
}
