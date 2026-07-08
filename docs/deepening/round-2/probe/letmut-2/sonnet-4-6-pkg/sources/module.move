module text::builder {
    use std::string::{Self, String};

    public fun join(parts: vector<String>, sep: String): String {
        let mut result = string::utf8(b"");
        let len = parts.length();
        let mut i = 0;
        while (i < len) {
            if (i > 0) {
                result.append(sep);
            };
            result.append(parts[i]);
            i = i + 1;
        };
        result
    }
}
