module string_append_red::tag {
    use std::string::String;

    // `+` is an integer-only built-in in Move; there is no String
    // concatenation operator.
    public fun join(a: String, b: String): String {
        a + b
    }
}
