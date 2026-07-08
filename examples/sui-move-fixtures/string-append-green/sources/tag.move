module string_append_green::tag {
    use std::string::String;

    // String concatenation is `append` (in place, through `&mut`).
    public fun join(mut a: String, b: String): String {
        a.append(b);
        a
    }
}
