module string_module_path_green::greet {
    use std::string::{Self, String};

    // The call form is the lowercase module path: `string::utf8`.
    public fun hello(): String {
        string::utf8(b"hello")
    }
}
