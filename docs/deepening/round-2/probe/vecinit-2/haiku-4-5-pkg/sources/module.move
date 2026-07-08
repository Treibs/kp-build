module math::fib {
    public fun first_n(n: u64): vector<u64> {
        let mut result = vector[];
        
        if (n == 0) {
            return result
        };
        
        result.push_back(0);
        
        if (n == 1) {
            return result
        };
        
        result.push_back(1);
        
        let mut i = 2;
        while (i < n) {
            let a = result[i - 1];
            let b = result[i - 2];
            result.push_back(a + b);
            i = i + 1;
        };
        
        result
    }
}
