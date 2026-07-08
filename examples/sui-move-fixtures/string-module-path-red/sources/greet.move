module string_module_path_red::greet {
    use std::string::String;

    // Rust-style associated-function path: Move 2024 parses `String::utf8`
    // as enum-variant construction, not a function call.
    public fun hello(): String {
        String::utf8(b"hello")
    }
}
